"""Rebuild the evidence tables from the preserved ZeroToViral snapshots.

The historical NLP specification is retained. Segmentation is a corrected rerun;
its results must not be represented as the original submitted model outputs.
"""
from pathlib import Path
from collections import Counter
import argparse
import ast
import hashlib
import importlib.metadata
import json
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.cache/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA, LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler

TABLES = ROOT / 'results/tables'
FIGURES = ROOT / 'results/figures'
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
CATEGORIES = {1:'Film & Animation',2:'Autos & Vehicles',10:'Music',15:'Pets & Animals',17:'Sports',19:'Travel & Events',20:'Gaming',22:'People & Blogs',23:'Comedy',24:'Entertainment',25:'News & Politics',26:'Howto & Style',27:'Education',28:'Science & Technology',29:'Nonprofits & Activism'}


def save_table(df, name):
    TABLES.mkdir(parents=True, exist_ok=True)
    df.to_csv(TABLES / (name + '.csv'), index=False, float_format='%.10g')
    return df


def save_figure(fig, name):
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(FIGURES / (name + '.png'), dpi=170, bbox_inches='tight')
    plt.close(fig)


def load_data():
    micro = pd.read_csv(ROOT / 'data/micro_clean.csv')
    large = pd.read_csv(ROOT / 'data/large_clean.csv')
    micro = micro.rename(columns={'post_hour':'publish_hour', 'duration_seconds':'duration_sec', 'desc_length':'desc_len'})
    micro['category_name'] = micro.category_id.map(CATEGORIES).fillna('Unknown')
    micro['source'] = 'micro'
    large['source'] = 'large'
    large['post_day'] = large.publish_weekday.map(dict(enumerate(DAYS)))
    return micro, large


def analysis_cohorts(micro, large):
    # Positive subscriber filter reconstructs the historical micro sample size.
    # This is explicit reconstruction, not a recovered original cleaning script.
    m = micro[(micro.view_count > 0) & micro.like_rate.between(0, 1) & micro.subscriber_count.between(1, 9999)].copy()
    l = large[(large.view_count > 0) & large.like_rate.between(0, 1) & (large.subscriber_count >= 10000)].copy()
    return m, l


def audit():
    micro, large = load_data()
    raw = pd.read_csv(ROOT / 'data/raw_collection.csv')
    m, l = analysis_cohorts(micro, large)
    rows = []
    for label, df in [('raw_collection',raw),('micro_snapshot',micro),('large_snapshot',large),('micro_analysis',m),('large_analysis',l)]:
        rows.append(dict(dataset=label, rows=len(df), unique_videos=df.video_id.nunique(), unique_channels=df.channel_id.nunique(), zero_views=int((df.view_count==0).sum()), zero_subscribers=int((df.subscriber_count==0).sum()), like_rate_above_one=int((df.like_rate>1).sum())))
    save_table(pd.DataFrame(rows), 'data_audit')
    steps=[('Saved micro snapshot',len(micro)),('Positive views',len(micro[micro.view_count>0])),('Valid like rate',len(micro[(micro.view_count>0)&micro.like_rate.between(0,1)])),('Positive subscribers below 10,000',len(m))]
    save_table(pd.DataFrame(steps,columns=['step','rows']), 'cohort_flow')
    coverage=[]
    for field in ['description','tags','top_comments_text','hashtags_from_title','hashtags_from_desc']:
        for label,df in [('micro_snapshot',micro),('micro_analysis',m)]:
            n=int(df[field].fillna('').astype(str).str.strip().ne('').sum())
            coverage.append(dict(dataset=label,field=field,nonempty=n,rows=len(df),coverage=n/len(df)))
    save_table(pd.DataFrame(coverage),'text_coverage')
    counts=m.groupby('post_day').size().reindex(DAYS,fill_value=0)
    save_table(counts.rename('videos').rename_axis('day').reset_index(),'posting_day_counts')
    save_table(m.groupby('category_name').agg(videos=('video_id','size'),channels=('channel_id','nunique'),median_views=('view_count','median')).reset_index(),'micro_categories')
    fig,ax=plt.subplots(figsize=(9,4.6)); bars=ax.bar(counts.index.str[:3],counts.values,color='#4263A6')
    ax.bar_label(bars,padding=3);ax.set(title='The micro sample is concentrated on Monday and Tuesday',ylabel='Video records (n = 1,035)');ax.spines[['top','right']].set_visible(False)
    save_figure(fig,'sampling_by_day')
    return m,l


def cluster():
    m,l=analysis_cohorts(*load_data())
    df=pd.concat([l,m],ignore_index=True)
    df['efficiency_ratio']=df.view_count/(df.subscriber_count+1)
    features=['efficiency_ratio','like_rate','duration_sec']
    df=df.dropna(subset=features).copy()
    X=StandardScaler().fit_transform(np.log1p(df[features]))
    pca=PCA(n_components=2)
    xp=pca.fit_transform(X)
    diagnostics=[]
    for k in range(2,9):
        model=KMeans(n_clusters=k,random_state=42,n_init=10).fit(xp)
        from sklearn.metrics import silhouette_score
        diagnostics.append(dict(k=k,inertia=model.inertia_,silhouette=silhouette_score(xp,model.labels_)))
    save_table(pd.DataFrame(diagnostics),'cluster_diagnostics')
    model=KMeans(n_clusters=4,random_state=42,n_init=10)
    df['cluster']=model.fit_predict(xp)
    summary=df.groupby('cluster').agg(videos=('video_id','size'),mean_efficiency=('efficiency_ratio','mean'),mean_like_rate=('like_rate','mean'),mean_duration_sec=('duration_sec','mean'),mean_subscribers=('subscriber_count','mean'),median_views=('view_count','median'),micro_videos=('source',lambda s:(s=='micro').sum())).reset_index()
    save_table(summary,'cluster_profiles_corrected')
    save_table(pd.DataFrame(pca.components_.T,index=features,columns=['PC1','PC2']).rename_axis('feature').reset_index(),'pca_loadings_corrected')
    save_table(pd.DataFrame({'component':['PC1','PC2'],'explained_variance_ratio':pca.explained_variance_ratio_}),'pca_variance_corrected')
    fig,axes=plt.subplots(1,2,figsize=(11,4.6))
    for c in sorted(df.cluster.unique()):
        mask=df.cluster.eq(c).to_numpy();axes[0].scatter(xp[mask,0],xp[mask,1],s=9,alpha=.5,label=f'Cluster {c}')
    axes[0].set(title='Corrected four-cluster rerun',xlabel='Principal component 1',ylabel='Principal component 2');axes[0].legend(markerscale=2,fontsize=8)
    dd=pd.DataFrame(diagnostics);axes[1].plot(dd.k,dd.silhouette,marker='o',color='#4263A6');axes[1].axvline(4,color='#C8614A',ls='--');axes[1].set(title='K = 4 retained for comparison with the submission',xlabel='Number of clusters',ylabel='Silhouette score')
    save_figure(fig,'clustering_corrected')


def parse_micro_tags(row):
    values=[]
    for col in ['hashtags_from_title','hashtags_from_desc']:
        if pd.notna(row[col]):values.extend(str(row[col]).split('|||'))
    return sorted({t.strip().lower().lstrip('#') for t in values if t.strip()})


def parse_large_tags(value):
    if pd.isna(value):return []
    parsed=ast.literal_eval(str(value))
    return sorted({str(t).strip().lower().lstrip('#') for t in parsed if str(t).strip()})


def tags():
    from mlxtend.frequent_patterns import apriori, association_rules
    from mlxtend.preprocessing import TransactionEncoder
    m,l=analysis_cohorts(*load_data())
    m['hashtag_list']=m.apply(parse_micro_tags,axis=1)
    l['hashtag_list']=l.all_hashtags.apply(parse_large_tags)
    med_v,med_l=m.view_count.median(),m.like_rate.median()
    m['quadrant']=np.select([(m.view_count>=med_v)&(m.like_rate>=med_l),(m.view_count>=med_v)&(m.like_rate<med_l),(m.view_count<med_v)&(m.like_rate>=med_l)],['Golden','Exposure Trap','Niche'],default='Ineffective')
    save_table(m.groupby('quadrant').size().rename('videos').reset_index(),'tag_quadrants')
    save_table(pd.DataFrame([dict(median_views=med_v,median_like_rate=med_l)]),'tag_thresholds')
    exploded=m.explode('hashtag_list').dropna(subset=['hashtag_list'])
    perf=exploded.groupby('hashtag_list').agg(videos=('video_id','size'),mean_like_rate=('like_rate','mean'),median_like_rate=('like_rate','median'),mean_views=('view_count','mean')).reset_index().rename(columns={'hashtag_list':'tag'})
    save_table(perf[perf.videos>=10].sort_values(['mean_like_rate','tag'],ascending=[False,True]),'tag_performance')
    summaries=[]
    for label,df in [('micro',m),('large',l)]:
        df['unique_hashtag_count']=df.hashtag_list.map(len)
        # Historical quantity comparisons are reconstructed from unique parsed hashtags.
        df['bin']=pd.cut(df.unique_hashtag_count,[-1,0,3,7,15,np.inf],labels=['0','1–3','4–7','8–15','16+'])
        out=df.groupby('bin',observed=False).agg(videos=('video_id','size'),median_views=('view_count','median'),median_like_rate=('like_rate','median')).reset_index()
        out.insert(0,'cohort',label);summaries.append(out)
    bins=pd.concat(summaries,ignore_index=True);save_table(bins,'hashtag_quantity')
    # Original correlation specification used stored hashtag_count, not unique counts.
    corr=[]
    for count_col in ['hashtag_count','unique_hashtag_count']:
        x=m[count_col].to_numpy(float);y=m.like_rate.to_numpy(float)
        for method,fn in [('pearson',stats.pearsonr),('spearman',stats.spearmanr)]:
            r,p=fn(x,y);corr.append(dict(count_definition=count_col,method=method,r=r,p=p,n=len(m)))
        z=np.column_stack([np.ones(len(m)),np.log1p(m.subscriber_count)])
        rx=x-z@np.linalg.lstsq(z,x,rcond=None)[0];ry=y-z@np.linalg.lstsq(z,y,rcond=None)[0]
        r=stats.pearsonr(rx,ry).statistic
        # One covariate: residual correlation inference uses n - 3 degrees of freedom.
        t=r*np.sqrt((len(m)-3)/(1-r*r));p=2*stats.t.sf(abs(t),len(m)-3)
        corr.append(dict(count_definition=count_col,method='partial_pearson_log1p_subscribers',r=r,p=p,n=len(m)))
    # Recover the working notebook's three-control specification separately.
    z=np.column_stack([np.ones(len(m)),m[['view_count','subscriber_count','duration_sec']].to_numpy(float)])
    x=m.hashtag_count.to_numpy(float);y=m.like_rate.to_numpy(float)
    rx=x-z@np.linalg.lstsq(z,x,rcond=None)[0];ry=y-z@np.linalg.lstsq(z,y,rcond=None)[0]
    r=stats.pearsonr(rx,ry).statistic;t=r*np.sqrt((len(m)-5)/(1-r*r))
    corr.append(dict(count_definition='hashtag_count',method='partial_pearson_views_subscribers_duration',r=r,p=2*stats.t.sf(abs(t),len(m)-5),n=len(m)))
    save_table(pd.DataFrame(corr),'hashtag_correlations')
    transactions=[]
    for zone in ['Golden','Exposure Trap','Niche']:
        subset=m[m.quadrant==zone];lists=[a for a in subset.hashtag_list if len(a)>1]
        te=TransactionEncoder();encoded=pd.DataFrame(te.fit_transform(lists),columns=te.columns_)
        encoded=encoded.loc[:,encoded.mean()>=.025]
        freq=apriori(encoded,min_support=.025,use_colnames=True)
        rules=association_rules(freq,metric='lift',min_threshold=1.3,num_itemsets=len(lists))
        for col in ['antecedents','consequents']:rules[col]=rules[col].apply(lambda x:' | '.join(sorted(x)))
        rules=rules[['antecedents','consequents','support','confidence','lift']].sort_values(['lift','support','antecedents','consequents'],ascending=[False,False,True,True])
        save_table(rules,'rules_'+zone.lower().replace(' ','_'))
        transactions.append(dict(quadrant=zone,videos=len(subset),eligible_transactions=len(lists),rules=len(rules),min_support=.025,min_lift=1.3))
    save_table(pd.DataFrame(transactions),'rule_denominators')
    fig,axes=plt.subplots(1,2,figsize=(10,4.4))
    for label,color in [('micro','#4263A6'),('large','#258574')]:
        b=bins[bins.cohort==label]
        axes[0].plot(b.bin.astype(str),100*b.median_like_rate,marker='o',label=label,color=color)
    axes[0].set(title='Like rate and hashtag quantity',xlabel='Unique hashtags per video',ylabel='Median like rate (%)');axes[0].legend()
    b=bins[bins.cohort=='micro'];bars=axes[1].bar(b.bin.astype(str),b.videos,color='#4263A6');axes[1].bar_label(bars,padding=3);axes[1].set(title='Micro sample size in each bin',xlabel='Unique hashtags per video',ylabel='Video records')
    save_figure(fig,'hashtag_quantity')


def golden_windows(m,l):
    perf=m.groupby(['post_day','publish_hour']).agg(micro_median_views=('view_count','median'),micro_videos=('video_id','size')).reset_index()
    perf['micro_rank']=perf.micro_median_views.rank(pct=True)
    density=l.groupby(['post_day','publish_hour']).size().rename('large_videos').reset_index()
    density['large_density_rank']=density.large_videos.rank(pct=True)
    out=perf.merge(density,on=['post_day','publish_hour'],how='left')
    out[['large_videos','large_density_rank']]=out[['large_videos','large_density_rank']].fillna(0)
    out['golden_score']=out.micro_rank-out.large_density_rank
    out['at_least_5_micro_videos']=out.micro_videos>=5
    return out.sort_values(['golden_score','post_day','publish_hour'],ascending=[False,True,True])


def timing():
    m,l=analysis_cohorts(*load_data())
    windows=save_table(golden_windows(m,l),'golden_windows')
    # Sensitivity view keeps original ranks and filters sparse slots afterward.
    save_table(windows[windows.micro_videos>=5],'golden_windows_min5')
    all_d=[]
    for label,lo,hi in [('Short duration (0–60s)',0,60),('Mid duration (60–600s)',60,600),('Long duration (>600s)',600,np.inf)]:
        mm=m[(m.duration_sec>lo)&(m.duration_sec<=hi)];ll=l[(l.duration_sec>lo)&(l.duration_sec<=hi)]
        w=golden_windows(mm,ll);w.insert(0,'duration_group',label);all_d.append(w)
    save_table(pd.concat(all_d,ignore_index=True),'golden_windows_by_duration')
    save_table(m.groupby('publish_hour').agg(videos=('video_id','size'),median_views=('view_count','median'),median_like_rate=('like_rate','median')).reset_index(),'posting_hours')
    dur=[]
    for label,df in [('micro',m),('large',l)]:
        group=pd.cut(df.duration_sec,[0,60,600,np.inf],labels=['0–60s','60–600s','>600s'])
        s=df.groupby(group,observed=False).agg(videos=('video_id','size'),median_views=('view_count','median'),median_like_rate=('like_rate','median')).reset_index();s.insert(0,'cohort',label);dur.append(s)
    save_table(pd.concat(dur,ignore_index=True),'duration_summary')
    top=windows.head(10).iloc[::-1]
    fig,ax=plt.subplots(figsize=(9,5.4));labels=[f'{d[:3]} {int(h):02}:00 UTC   (n={int(n)})' for d,h,n in zip(top.post_day,top.publish_hour,top.micro_videos)]
    ax.barh(labels,top.golden_score,color=['#C8614A' if n<5 else '#4263A6' for n in top.micro_videos]);ax.set(title='Highest timing scores often have very few observations',xlabel='Micro performance percentile − large posting-density percentile');ax.spines[['top','right']].set_visible(False)
    save_figure(fig,'timing_sample_sizes')


# Stopword vocabulary below is retained from the submitted NLP notebook.
BASE_STOPWORDS = {
    "the","and","is","to","of","in","for","on","with","this","that","it","my","your",
    "a","an","at","be","are","was","were","am","as","by","from","or","if","but","so",
    "me","we","you","they","he","she","them","our","us","their","his","her","i","im",
    "its","into","out","up","down","about","just","can","will","would","could","should",
    "have","has","had","do","does","did","not","no","yes","all","any","some","more",
    "very","really","get","got","go","goes","going","come","came","make","made","take",
    "today","day","days","one","two","first","new","latest","best","good","nice"
}

GENERIC_PLATFORM_STOPWORDS = {
    "video","videos","vlog","vlogs","study","studying","youtube","youtuber","yt","ytshorts",
    "short","shorts","shortvideo","shortvideos","viral","viralshort","viralvideo","subscribe",
    "subscriber","channel","content","creator","creators","upload","uploads","posted","posting",
    "mini","minivlog","daily","dailyvlog","dailylife","reel","reels","fyp","trend","trending",
    "comment","comments","like","likes","share","sharing","watch","watching","intro"
}

LIGHT_KEEP_WORDS = {"life","story","journey","family","love","real","ideas","beginner","routine"}

CUSTOM_STOPWORDS = (BASE_STOPWORDS | GENERIC_PLATFORM_STOPWORDS) - LIGHT_KEEP_WORDS

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize_filtered(text, stopwords=CUSTOM_STOPWORDS, min_len=3):
    text = clean_text(text)
    tokens = [w for w in text.split() if len(w) >= min_len and w not in stopwords]
    return tokens


def nlp():
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
    nltk.data.path.insert(0,str(ROOT/'.cache/nltk_data'))
    try:
        sia=SentimentIntensityAnalyzer()
    except LookupError as e:
        raise RuntimeError('Run: python -m nltk.downloader -d .cache/nltk_data vader_lexicon') from e
    df,_=load_data()  # Preserve all 1,090 records and original 545/545 labels for historical NLP.
    df['content_text']=df.video_title.fillna('')+' '+df.description.fillna('')
    df['full_text']=df.content_text+' '+df.top_comments_text.fillna('')
    df['sentiment']=df.full_text.apply(lambda s:sia.polarity_scores(s)['compound'])
    df['strongly_positive']=df.sentiment>.8
    df['content_only_sentiment']=df.content_text.apply(lambda s:sia.polarity_scores(s)['compound'])
    summary=df.groupby('like_rate_group').agg(videos=('video_id','size'),mean_compound=('sentiment','mean'),strongly_positive_share=('strongly_positive','mean'),mean_content_only_compound=('content_only_sentiment','mean')).reset_index()
    save_table(summary,'sentiment')
    counters={g:Counter(t for text in sub.content_text for t in tokenize_filtered(text)) for g,sub in df.groupby('like_rate_group')}
    words=sorted(set(counters['High'])|set(counters['Low']))
    n=df.like_rate_group.value_counts()
    keyword=pd.DataFrame([dict(word=w,high_frequency=counters['High'][w]/n['High'],low_frequency=counters['Low'][w]/n['Low'],difference=counters['High'][w]/n['High']-counters['Low'][w]/n['Low']) for w in words])
    save_table(keyword.sort_values(['difference','word'],ascending=[False,True]),'distinctive_keywords')
    distributions=[];topics=[];entropy=[]
    for group,sub in df.groupby('like_rate_group'):
        vectorizer=CountVectorizer(stop_words=sorted(CUSTOM_STOPWORDS),max_features=1000,min_df=2)
        X=vectorizer.fit_transform(sub.content_text.apply(clean_text))
        lda=LatentDirichletAllocation(n_components=5,random_state=42,learning_method='batch')
        mixture=lda.fit_transform(X);vocab=vectorizer.get_feature_names_out();dominant=mixture.argmax(axis=1)
        shares=pd.Series(dominant).value_counts(normalize=True).reindex(range(5),fill_value=0)
        for idx in range(5):
            distributions.append(dict(group=group,topic=idx+1,share=shares[idx],videos=int((dominant==idx).sum())))
            topics.append(dict(group=group,topic=idx+1,top_words=', '.join(vocab[lda.components_[idx].argsort()[::-1][:10]])))
        entropy.append(dict(group=group,entropy=-(shares*np.log(shares+1e-12)).sum(),max_topic_share=shares.max()))
        positive=sub[sub.strongly_positive]
        pairs=Counter()
        for text in positive.full_text:
            tokens=tokenize_filtered(text);pairs.update(' '.join(x) for x in zip(tokens,tokens[1:]))
        bigrams=pd.DataFrame(pairs.items(),columns=['bigram','count']).sort_values(['count','bigram'],ascending=[False,True])
        save_table(bigrams,'positive_full_text_bigrams_'+group.lower())
    save_table(pd.DataFrame(distributions),'topic_distributions');save_table(pd.DataFrame(topics),'topic_terms');save_table(pd.DataFrame(entropy),'topic_concentration')
    fig,axes=plt.subplots(1,2,figsize=(10,4.4));colors=['#4263A6','#A7B7D4']
    bars=axes[0].bar(summary.like_rate_group,summary.mean_compound,color=colors);axes[0].bar_label(bars,fmt='%.3f',padding=4);axes[0].set(title='Combined title, description and comments',ylabel='Mean VADER compound score',ylim=(0,.52))
    bars=axes[1].bar(summary.like_rate_group,100*summary.strongly_positive_share,color=colors);axes[1].bar_label(bars,fmt='%.1f%%',padding=4);axes[1].set(title='Strongly positive text (compound > 0.8)',ylabel='Share of videos (%)',ylim=(0,42))
    save_figure(fig,'sentiment_comparison')


def provenance():
    datasets={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'data').glob('*.csv'))}
    packages={p:importlib.metadata.version(p) for p in ['pandas','numpy','scipy','scikit-learn','matplotlib','nltk','mlxtend']}
    payload={'python':sys.version.split()[0],'packages':packages,'data_sha256':datasets,'random_state':42,'cluster_specification':'views/(subscribers+1), log1p, StandardScaler, PCA(2), KMeans(4,n_init=10)','nlp_cohort':'original 1090 rows, original 545/545 labels','quantitative_cohorts':'1035 micro, 1174 large; explicit positive-subscriber filter','timing_minimum_support_sensitivity':5}
    payload['analysis_source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    lexicon=ROOT/'.cache/nltk_data/sentiment/vader_lexicon.zip'
    if lexicon.exists():payload['vader_lexicon_zip_sha256']=hashlib.sha256(lexicon.read_bytes()).hexdigest()
    (ROOT/'results/run_manifest.json').write_text(json.dumps(payload,indent=2)+'\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--section',choices=['all','audit','cluster','nlp','tags','timing'],default='all')
    args=parser.parse_args()
    for name,fn in [('audit',audit),('cluster',cluster),('nlp',nlp),('tags',tags),('timing',timing)]:
        if args.section in ['all',name]:
            print('Running',name,flush=True);fn()
    provenance();print('Evidence written to results/',flush=True)


if __name__=='__main__':main()
