from main import extract_lead_time, backfill_done_cards


class MockCompleted:
    data = {'id': '5b900506-45e5-4080-b02e-a0a4c45a2609', 'changed_at': '2018-09-05T16:32:07.009Z', 'primary_id': 3191, 'version': 'v1', 'member_id': '59c02473-94a2-4ee7-8ad6-d97f350b4854', 'actions': [{'id': 3209, 'entity_type': 'story', 'action': 'update', 'name': 'Extract lead time and cycle time from the beta Clubhouse API for analysis', 'story_type': 'feature', 'app_url': 'https://app.clubhouse.io/oao/story/3191', 'changes': {'completed_at': {'new': '2018-09-05T16:32:06Z'}, 'completed': {'new': True, 'old': False}, 'workflow_state_id': {'new': 500000005, 'old': 500000007}}}], 'references': [{'id': 500000005, 'entity_type': 'workflow-state', 'name': 'Completed', 'type': 'done'}, {'id': 500000007, 'entity_type': 'workflow-state', 'name': 'Build', 'type': 'started'}]}
    
    def get_json(self, force):
        return self.data


print("Returned:", backfill_done_cards(None))

