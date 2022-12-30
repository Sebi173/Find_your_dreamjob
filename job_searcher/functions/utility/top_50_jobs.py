def sort_top_50_jobs(list_jobs_with_scores):
    jobs_scores_list = sorted(list_jobs_with_scores, key=lambda x:x["score"], reverse=True)

    return jobs_scores_list
