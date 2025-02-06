from jobs.scores import Scores


class JobFactory:
    @staticmethod
    def get_all(jobs_str):
        jobs = []
        for job_str in jobs_str:
            if job_str == 'Scores':
                jobs.append(Scores())
        return jobs