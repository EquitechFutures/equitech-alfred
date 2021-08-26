import datetime as dt

from notion.notion.client import NotionClient


class Alfred:
    def __init__(self, token_v2):
        self.client = NotionClient(token_v2)

    def _bulk_copy(self, db, src_page_id, user_ids):
        src_page = self.client.get_block(src_page_id)

        for user_id in user_ids:
            print(f"Creating a copy for {user_id}")
            new_page = db.collection.add_row(source_block_id=src_page.id)
            new_page.assigned_to = user_id
            new_page.icon = src_page.icon
            new_page.title = src_page.title
            new_page.deadline = src_page.deadline
            new_page.course = src_page.course
            new_page.review_status = "To Review"

    def _share_page(self, page):
        now = dt.datetime.now()
        new_role = "comment_only"
        all_assigned_emails = [assignee.email for assignee in page.assigned_to]
        deadline = page.deadline.start if page.deadline else dt.datetime(2022, 1, 1)
        deadline = self.absolute_deadline(deadline)

        if len(all_assigned_emails) > 0 and now < deadline:
            new_role = "read_and_write"

        page_details = self.client.get_block(page.id)
        page_details_raw = page_details.get()
        page_details_raw["permissions"] = [
            {
                "role": new_role,
                "type": "user_permission",
                "user_id": user.id,
            }
            for user in page.assigned_to
        ]

        page_details.set(path=["permissions"], value=page_details_raw["permissions"])

        return {
            "page_id": page.id,
            "page_name": page.title,
            "assigned": all_assigned_emails,
            "new_role": new_role,
            "deadline": deadline,
        }

    def assign_all(
        self,
        template_db_id: str,
        target_db_id: str,
        user_ids: list,
        filter_template="READY",
    ):
        template_db = self.client.get_collection_view(template_db_id)
        target_db = self.client.get_collection_view(target_db_id)

        for template in template_db.collection.get_rows(search=filter_template):
            print(f'Template "{template.title}" is {template.status}')
            self._bulk_copy(target_db, template.id, user_ids)
            template.status = "ASSIGNED"

    def auto_share_pages(self, target_db_id, filter_db="To Review"):
        target_db = self.client.get_collection_view(target_db_id)
        print(f'Auto sharing pages in "{target_db.name}"')
        for row in target_db.collection.get_rows(search=filter_db):
            yield self._share_page(row)

    @staticmethod
    def absolute_deadline(deadline):
        if isinstance(deadline, dt.datetime):
            pass
        elif isinstance(deadline, dt.date):
            # convert date to datetime (end of day hh:mm:ss)
            deadline_parts = deadline.timetuple()[:6]
            deadline = dt.datetime(*deadline_parts) + dt.timedelta(
                days=1, microseconds=-1
            )
        return deadline
