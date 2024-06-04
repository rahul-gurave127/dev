import os
from datetime import date
from jira import JIRA
import pandas as pd
from config import username, password


class CurrentSprint:
    def __init__(self):
        self.headers = [["ISSUE_TYPE", "PSA_ID", "LINKED_ISSUES", "HARMAN_ID", "SUMMARY","STATUS","RESOLUTION","QA_COMMENTS"]]
        self.base_url = {'server': "https://jira.labs.hosting.cerence.net"}
        self.issue_types =  ["Bug", "Requirement", "Story"]
        self.active_sprint = None
        self.qacomment = None
        self.linked_issues = []
    
    def jira_login(self):
        """Login to jira"""
        try:
            jira_auth = JIRA(options=self.base_url, basic_auth=(username, password))
            print("User login successfully")
            return jira_auth
        except IOError:
            print("Authentication Error: Incorrect username or password..!!")
    
    def get_product_issue_link(self, issue):
        product_issue_link = issue.fields.customfield_15809
        if product_issue_link is not None:
           return product_issue_link.split('/')[-1]
        return None

    def get_current_sprint_req(self):
        jsession  = self.jira_login()
        self.active_sprint = '_'.join(str(jsession.sprint("12921")).split()[1:])
        for sprint_issue in jsession.search_issues("project = 'PSA Caruso R2' AND issuetype in (Story, Requirement, Bug) AND Sprint  in openSprints()",  maxResults=100):
            print(f"Fetching details for {sprint_issue.fields.issuetype}: {sprint_issue.key}...")
            product_issue_link = self.get_product_issue_link(sprint_issue)
            if str(sprint_issue.fields.status) == "Closed" and str(sprint_issue.fields.resolution) == "Done":
                self.qacomment = "Tested and Working Fine"
            elif str(sprint_issue.fields.status) in ("Closed", "Resolved") and str(sprint_issue.fields.resolution) == "Won't Do":
                self.qacomment = "Ticket Assign To Customer"
            elif str(sprint_issue.fields.status) == "Resolved" and str(sprint_issue.fields.resolution) in ("Done", "Cannot Reproduce"):
                self.qacomment = "Need To Test"
            else:
                self.qacomment = "Waiting For Fix"

            if str(sprint_issue.fields.issuetype) in ("Story", "Requirement") and str(sprint_issue.fields.status) not in ("Resolved", "Closed"):
                get_linked_issues = jsession.issue(sprint_issue.key)
                for issueLinked in get_linked_issues.fields.issuelinks:
                    if hasattr(issueLinked, "outwardIssue") and str(issueLinked.outwardIssue.fields.issuetype.name) != 'Story' and str(issueLinked.outwardIssue.fields.status.name) not in ('Resolved', 'Closed'):
                        # print(f"Out:{issueLinked.outwardIssue.key} => {issueLinked.outwardIssue.fields.status.name}")
                        self.linked_issues.append(issueLinked.outwardIssue.key)
                        product_issue_link = self.get_product_issue_link(jsession.issue(issueLinked.outwardIssue.key))
                        self.headers.append([sprint_issue.fields.issuetype, sprint_issue.key, issueLinked.outwardIssue.key, product_issue_link, sprint_issue.fields.summary, sprint_issue.fields.status, sprint_issue.fields.resolution, self.qacomment])
                    if hasattr(issueLinked, "inwardIssue") and str(issueLinked.inwardIssue.fields.issuetype.name) != 'Story' and str(issueLinked.inwardIssue.fields.status.name) not in ('Resolved', 'Closed'):
                            # print(f"{issueLinked.inwardIssue.key} => {issueLinked.inwardIssue.fields.status.name}")
                            self.linked_issues.append(issueLinked.inwardIssue.key)
                            product_issue_link = self.get_product_issue_link(jsession.issue(issueLinked.inwardIssue.key))
                            self.headers.append([sprint_issue.fields.issuetype, sprint_issue.key, issueLinked.inwardIssue.key, product_issue_link, sprint_issue.fields.summary,sprint_issue.fields.status, sprint_issue.fields.resolution, self.qacomment])                      
            if str(sprint_issue.fields.issuetype) == "Bug" and sprint_issue.key not in self.linked_issues:
                self.headers.append([sprint_issue.fields.issuetype, sprint_issue.key, "NA" , product_issue_link, sprint_issue.fields.summary, sprint_issue.fields.status, sprint_issue.fields.resolution, self.qacomment])
        return self.headers
    
    def generate_report(self, sprint_candidate):
        """To generate a report in Excel format using pandas"""
        df = pd.DataFrame(sprint_candidate)
        sprint_dir = u"{0}\\PSA_Sprints\\{1}".format(os.path.expanduser('~'), self.active_sprint)
        # Checking if sprint_dir exist or not. If not then create it.
        if not os.path.exists(sprint_dir):
            try:
                os.mkdir(sprint_dir)
                print("{0} created..".format(sprint_dir))
            except IOError:
                print('Failed to create directory {0}'.format(sprint_dir))
        filepath = u"{0}\\{1}_Candidate_List_{2}".format(sprint_dir, self.active_sprint, date.today())

        try:
            # Converting dataframe object in to Excel file.
            df.to_excel("{}.xlsx".format(filepath), index=False, header=False)
            print(f"Report Generated:'{filepath}.xlsx'")
        except IOError:
            print("DataFrame fail to stored in excel file.")
        
        return 0


if __name__ == '__main__':
    sprint = CurrentSprint()
    headers = sprint.get_current_sprint_req()
    sprint.generate_report(headers)
    print("Done..!")
