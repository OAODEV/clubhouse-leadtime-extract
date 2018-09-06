.PHONY: deploy
deploy:
	gcloud beta functions deploy extract_lead_time \
		--runtime python37 \
		--trigger-http \
		--set-env-vars CLUBHOUSE_API_TOKEN=$(shell echo $$CLUBHOUSE_API_TOKEN)


.PHONY: deploy-backfill
deploy-backfill:
	gcloud beta functions deploy backfill_done_cards \
		--runtime python37 \
		--trigger-http \
		--set-env-vars CLUBHOUSE_API_TOKEN=$(shell echo $$CLUBHOUSE_API_TOKEN) \
		--timeout 540
