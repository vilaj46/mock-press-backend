from googleapiclient import discovery
from pprint import pprint


from Sheets import Create_Database


class Database():

    service = {}
    admin_service = {}

    customers = []

    def get_admins(self):
        self.admin_service = Create_Database()

        # The spreadsheet to request.
        spreadsheet_id = '1KLmwdD1ohibCaYWZtYFjJZi0RAp52CJyRTCZgDkTUkk'

        admins = self.admin_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range='Admins')
        admins_response = admins.execute()
        admins = self.create_admins(admins_response['values'])
        return admins

    def create_admins(self, values):
        keys = values[0]
        data = values[1]
        admins = []
        admin_dict = {}
        for i in range(len(keys)):
            key = keys[i]
            admin_dict[key] = data[i]
        admins.append(admin_dict)
        return admins

    def __init__(self):
        self.service = Create_Database()

        # The spreadsheet to request.
        spreadsheet_id = '1KLmwdD1ohibCaYWZtYFjJZi0RAp52CJyRTCZgDkTUkk'

        # The ranges to retrive from the spreadsheet.
        ranges = []  # Update placeholder value.

        # True if grid data should be returned.
        # This parameter is ignored if a field
        # mask was set in the request.
        include_grid_data = False  # Update placeholder value.

        # request = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id)
        customers = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range='Customers')
        customers_response = customers.execute()

        users = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range='Users')
        users_response = users.execute()

        jobs = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range='Jobs')
        jobs_response = jobs.execute()

        # Organize data
        organized_customers = self.organize_db_selection(customers_response)
        organized_users = self.organize_users(users_response)
        organized_jobs = self.organize_jobs(jobs_response)

        users_with_jobs = self.put_jobs_into_users(
            organized_users, organized_jobs)

        customers_with_users = self.put_users_into_customers(
            organized_customers, users_with_jobs
        )

        self.customers = customers_with_users

    def get_customers(self):
        return {
            'customers': self.customers
        }

    def put_users_into_customers(self, customers, users):
        for i in range(len(customers)):
            customer = customers[i]
            customer_id = customer['_id']

            try:
                # customers[i] =
                customers[i]['users'] = users[customer_id]
            except:
                do = 'nothing'
        return customers

    def put_jobs_into_users(self, users, jobs):
        # Users is a dict
        user_keys = users.keys()
        for key in user_keys:
            # Each key is an array
            current_customer = key

            # for user in users[current_customer]:
            for i in range(len(users[current_customer])):
                user = users[current_customer][i]
                try:
                    if user['jobs']:
                        user_jobs = jobs[user['_id']]
                        users[current_customer][i]['jobs'] = user_jobs
                except:
                    do = 'nothing'
        return users

    def organize_users(self, users):
        users_dict = {}
        users_list = users['values']
        keys = users_list[0]

        for i in range(1, len(users_list)):
            current_user = users_list[i]  # List
            user_dict = {}
            for j in range(0, len(current_user)):
                key = keys[j]
                value = current_user[j]
                user_dict[key] = value
            user_id = user_dict['customer']

            try:
                users_dict[user_id].append(user_dict)
            except:
                users_dict[user_id] = [user_dict]

        return users_dict

    def organize_jobs(self, jobs):
        jobs_dict = {}
        job_list = jobs['values']
        keys = job_list[0]

        for i in range(1, len(job_list)):
            current_job = job_list[i]  # List
            job_dict = {}
            for j in range(0, len(current_job)):
                key = keys[j]
                value = current_job[j]
                job_dict[key] = value

            user_id = job_dict['u_id']
            try:
                jobs_dict[user_id].append(job_dict)
            except:
                jobs_dict[user_id] = [job_dict]

        return jobs_dict

    def organize_db_selection(self, selection):
        selection_values = selection['values']
        keys = selection_values[0]  # Row 1
        l = []

        for i in range(1, len(selection_values)):
            values = selection_values[i]
            dict_obj = {}
            for j in range(0, len(values)):
                key = keys[j]
                value = values[j]
                dict_obj[key] = value
            l.append(dict_obj)

        return l
