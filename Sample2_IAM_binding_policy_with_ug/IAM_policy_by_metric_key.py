#JLL
import json
import requests
import os
import urllib3
import time
#import re
#from json import JSONEncoder
#import csv
import sys

##################################
### Environment variables
##################################
Account_Urn=os.getenv('DT_OAUTH_ACCOUNT_URN') #OAuth Account URN. OAuth variables are required when integrating with OAuth.
AccountUiid=Account_Urn.split(":")[2]
Client_ID=os.getenv('DT_OAUTH_CLIENT_ID') #ID	OAuth Client ID.
Client_Secret=os.getenv('DT_OAUTH_CLIENT_SECRET') #OAuth Client Secret
SSO_Endpoint=os.getenv('DT_OAUTH_SSO_ENDPOINT') #OAuth SSO endpoint with scope : account-idm-write account-idm-read

LIST=['cloud.gcp.agent_googleapis_com.agent.gae_app.api_request_count', 'cloud.gcp.agent_googleapis_com.agent.gae_app.log_entry_count', 'cloud.gcp.agent_googleapis_com.agent.gae_app.log_entry_retry_count', 'cloud.gcp.agent_googleapis_com.agent.gae_app.memory_usage', 'cloud.gcp.agent_googleapis_com.agent.gae_app.monitoring.point_count', 'cloud.gcp.agent_googleapis_com.agent.gae_app.request_count', 'cloud.gcp.agent_googleapis_com.agent.gae_app.streamspace_size', 'cloud.gcp.agent_googleapis_com.agent.gae_app.uptime.count', 'cloud.gcp.appengine_googleapis_com.http.server.dos_intercept_count', 'cloud.gcp.appengine_googleapis_com.http.server.quota_denial_count', 'cloud.gcp.appengine_googleapis_com.http.server.response_count', 'cloud.gcp.appengine_googleapis_com.http.server.response_latencies', 'cloud.gcp.appengine_googleapis_com.http.server.response_style_count', 'cloud.gcp.appengine_googleapis_com.system.billed_instance_estimate_count.gauge', 'cloud.gcp.appengine_googleapis_com.system.cpu.usage', 'cloud.gcp.appengine_googleapis_com.system.instance_count.gauge', 'cloud.gcp.appengine_googleapis_com.system.memory.usage', 'cloud.gcp.appengine_googleapis_com.system.network.received_bytes_count', 'cloud.gcp.appengine_googleapis_com.system.network.sent_bytes_count', 'cloud.gcp.autoscaler_googleapis_com.capacity', 'cloud.gcp.autoscaler_googleapis_com.current_utilization', 'cloud.gcp.bigquery_googleapis_com.job.num_in_flight', 'cloud.gcp.bigquery_googleapis_com.query.count.gauge', 'cloud.gcp.bigquery_googleapis_com.query.execution_times', 'cloud.gcp.bigquery_googleapis_com.slots.allocated', 'cloud.gcp.bigquery_googleapis_com.slots.total_allocated_for_reservation', 'cloud.gcp.bigquerybiengine_googleapis_com.model.inflight_requests', 'cloud.gcp.bigquerybiengine_googleapis_com.model.request_count', 'cloud.gcp.bigquerybiengine_googleapis_com.model.request_latencies', 'cloud.gcp.bigquerybiengine_googleapis_com.reservation.total_bytes', 'cloud.gcp.bigquerybiengine_googleapis_com.reservation.used_bytes', 'cloud.gcp.bigtable_googleapis_com.cluster.cpu_load', 'cloud.gcp.bigtable_googleapis_com.cluster.cpu_load_hottest_node', 'cloud.gcp.bigtable_googleapis_com.cluster.node_count.gauge', 'cloud.gcp.bigtable_googleapis_com.cluster.storage_utilization', 'cloud.gcp.bigtable_googleapis_com.disk.bytes_used', 'cloud.gcp.bigtable_googleapis_com.disk.per_node_storage_capacity', 'cloud.gcp.bigtable_googleapis_com.disk.storage_capacity', 'cloud.gcp.bigtable_googleapis_com.replication.latency', 'cloud.gcp.bigtable_googleapis_com.replication.max_delay', 'cloud.gcp.bigtable_googleapis_com.server.error_count', 'cloud.gcp.bigtable_googleapis_com.server.latencies', 'cloud.gcp.bigtable_googleapis_com.server.modified_rows_count', 'cloud.gcp.bigtable_googleapis_com.server.multi_cluster_failovers_count', 'cloud.gcp.bigtable_googleapis_com.server.received_bytes_count', 'cloud.gcp.bigtable_googleapis_com.server.request_count', 'cloud.gcp.bigtable_googleapis_com.server.returned_rows_count', 'cloud.gcp.bigtable_googleapis_com.server.sent_bytes_count', 'cloud.gcp.bigtable_googleapis_com.table.bytes_used', 'cloud.gcp.cloudfunctions_googleapis_com.function.active_instances', 'cloud.gcp.cloudfunctions_googleapis_com.function.execution_count', 'cloud.gcp.cloudfunctions_googleapis_com.function.execution_times', 'cloud.gcp.cloudfunctions_googleapis_com.function.network_egress.count', 'cloud.gcp.cloudfunctions_googleapis_com.function.user_memory_bytes', 'cloud.gcp.cloudsql_googleapis_com.database.available_for_failover', 'cloud.gcp.cloudsql_googleapis_com.database.cpu.reserved_cores', 'cloud.gcp.cloudsql_googleapis_com.database.cpu.usage_time.count', 'cloud.gcp.cloudsql_googleapis_com.database.cpu.utilization', 'cloud.gcp.cloudsql_googleapis_com.database.disk.bytes_used', 'cloud.gcp.cloudsql_googleapis_com.database.disk.quota', 'cloud.gcp.cloudsql_googleapis_com.database.disk.read_ops_count', 'cloud.gcp.cloudsql_googleapis_com.database.disk.utilization', 'cloud.gcp.cloudsql_googleapis_com.database.disk.write_ops_count', 'cloud.gcp.cloudsql_googleapis_com.database.instance_state', 'cloud.gcp.cloudsql_googleapis_com.database.memory.quota', 'cloud.gcp.cloudsql_googleapis_com.database.memory.total_usage', 'cloud.gcp.cloudsql_googleapis_com.database.memory.usage', 'cloud.gcp.cloudsql_googleapis_com.database.memory.utilization', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.innodb_buffer_pool_pages_dirty', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.innodb_buffer_pool_pages_free', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.innodb_buffer_pool_pages_total', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.innodb_data_fsyncs.count', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.innodb_os_log_fsyncs.count', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.innodb_pages_read.count', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.innodb_pages_written.count', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.queries.count', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.questions.count', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.received_bytes_count', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.replication.available_for_failover', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.replication.last_io_errno', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.replication.last_sql_errno', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.replication.seconds_behind_master', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.replication.slave_io_running_state', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.replication.slave_sql_running_state', 'cloud.gcp.cloudsql_googleapis_com.database.mysql.sent_bytes_count', 'cloud.gcp.cloudsql_googleapis_com.database.network.connections', 'cloud.gcp.cloudsql_googleapis_com.database.network.received_bytes_count', 'cloud.gcp.cloudsql_googleapis_com.database.network.sent_bytes_count', 'cloud.gcp.cloudsql_googleapis_com.database.postgresql.num_backends', 'cloud.gcp.cloudsql_googleapis_com.database.postgresql.replication.replica_byte_lag', 'cloud.gcp.cloudsql_googleapis_com.database.postgresql.transaction_count', 'cloud.gcp.cloudsql_googleapis_com.database.replication.replica_lag', 'cloud.gcp.cloudsql_googleapis_com.database.up', 'cloud.gcp.cloudsql_googleapis_com.database.uptime.count', 'cloud.gcp.cloudtasks_googleapis_com.api.request_count', 'cloud.gcp.cloudtasks_googleapis_com.queue.depth', 'cloud.gcp.cloudtasks_googleapis_com.queue.task_attempt_count', 'cloud.gcp.cloudtasks_googleapis_com.queue.task_attempt_delays', 'cloud.gcp.composer_googleapis_com.environment.api.request_count', 'cloud.gcp.composer_googleapis_com.environment.api.request_latencies', 'cloud.gcp.composer_googleapis_com.environment.dag_processing.parse_error_count', 'cloud.gcp.composer_googleapis_com.environment.dag_processing.processes', 'cloud.gcp.composer_googleapis_com.environment.dag_processing.total_parse_time', 'cloud.gcp.composer_googleapis_com.environment.dagbag_size', 'cloud.gcp.composer_googleapis_com.environment.database_health', 'cloud.gcp.composer_googleapis_com.environment.executor.open_slots', 'cloud.gcp.composer_googleapis_com.environment.executor.running_tasks', 'cloud.gcp.composer_googleapis_com.environment.finished_task_instance_count', 'cloud.gcp.composer_googleapis_com.environment.healthy', 'cloud.gcp.composer_googleapis_com.environment.num_celery_workers', 'cloud.gcp.composer_googleapis_com.environment.scheduler_heartbeat_count', 'cloud.gcp.composer_googleapis_com.environment.task_queue_length', 'cloud.gcp.composer_googleapis_com.environment.worker.pod_eviction_count', 'cloud.gcp.compute_googleapis_com.firewall.dropped_bytes_count', 'cloud.gcp.compute_googleapis_com.firewall.dropped_packets_count', 'cloud.gcp.compute_googleapis_com.guest.cpu.runnable_task_count.gauge', 'cloud.gcp.compute_googleapis_com.guest.cpu.usage_time.count', 'cloud.gcp.compute_googleapis_com.guest.disk.bytes_used', 'cloud.gcp.compute_googleapis_com.guest.disk.io_time.count', 'cloud.gcp.compute_googleapis_com.guest.disk.merged_operation_count', 'cloud.gcp.compute_googleapis_com.guest.disk.operation_bytes_count', 'cloud.gcp.compute_googleapis_com.guest.disk.operation_count', 'cloud.gcp.compute_googleapis_com.guest.disk.operation_time.count', 'cloud.gcp.compute_googleapis_com.guest.disk.queue_length', 'cloud.gcp.compute_googleapis_com.guest.disk.weighted_io_time.count', 'cloud.gcp.compute_googleapis_com.guest.memory.anonymous_used', 'cloud.gcp.compute_googleapis_com.guest.memory.bytes_used', 'cloud.gcp.compute_googleapis_com.guest.memory.dirty_used', 'cloud.gcp.compute_googleapis_com.guest.memory.page_cache_used', 'cloud.gcp.compute_googleapis_com.guest.memory.unevictable_used', 'cloud.gcp.compute_googleapis_com.guest.system.problem_count', 'cloud.gcp.compute_googleapis_com.guest.system.problem_state', 'cloud.gcp.compute_googleapis_com.guest.system.uptime', 'cloud.gcp.compute_googleapis_com.instance.cpu.reserved_cores', 'cloud.gcp.compute_googleapis_com.instance.cpu.scheduler_wait_time.count', 'cloud.gcp.compute_googleapis_com.instance.cpu.usage_time.count', 'cloud.gcp.compute_googleapis_com.instance.cpu.utilization', 'cloud.gcp.compute_googleapis_com.instance.disk.read_bytes_count', 'cloud.gcp.compute_googleapis_com.instance.disk.read_ops_count', 'cloud.gcp.compute_googleapis_com.instance.disk.write_bytes_count', 'cloud.gcp.compute_googleapis_com.instance.disk.write_ops_count', 'cloud.gcp.compute_googleapis_com.instance.integrity.early_boot_validation_status', 'cloud.gcp.compute_googleapis_com.instance.integrity.late_boot_validation_status', 'cloud.gcp.compute_googleapis_com.instance.memory.balloon.ram_size', 'cloud.gcp.compute_googleapis_com.instance.memory.balloon.ram_used', 'cloud.gcp.compute_googleapis_com.instance.memory.balloon.swap_in_bytes_count', 'cloud.gcp.compute_googleapis_com.instance.memory.balloon.swap_out_bytes_count', 'cloud.gcp.compute_googleapis_com.instance.network.received_bytes_count', 'cloud.gcp.compute_googleapis_com.instance.network.received_packets_count', 'cloud.gcp.compute_googleapis_com.instance.network.sent_bytes_count', 'cloud.gcp.compute_googleapis_com.instance.network.sent_packets_count', 'cloud.gcp.compute_googleapis_com.instance.uptime_total', 'cloud.gcp.compute_googleapis_com.instance.uptime.count', 'cloud.gcp.dataflow_googleapis_com.job.billable_shuffle_data_processed', 'cloud.gcp.dataflow_googleapis_com.job.current_num_vcpus', 'cloud.gcp.dataflow_googleapis_com.job.current_shuffle_slots', 'cloud.gcp.dataflow_googleapis_com.job.data_watermark_age', 'cloud.gcp.dataflow_googleapis_com.job.elapsed_time', 'cloud.gcp.dataflow_googleapis_com.job.element_count.gauge', 'cloud.gcp.dataflow_googleapis_com.job.elements_produced_count', 'cloud.gcp.dataflow_googleapis_com.job.estimated_byte_count.gauge', 'cloud.gcp.dataflow_googleapis_com.job.estimated_bytes_produced_count', 'cloud.gcp.dataflow_googleapis_com.job.is_failed', 'cloud.gcp.dataflow_googleapis_com.job.per_stage_data_watermark_age', 'cloud.gcp.dataflow_googleapis_com.job.per_stage_system_lag', 'cloud.gcp.dataflow_googleapis_com.job.pubsub.read_count', 'cloud.gcp.dataflow_googleapis_com.job.pubsub.read_latencies', 'cloud.gcp.dataflow_googleapis_com.job.pubsub.write_count', 'cloud.gcp.dataflow_googleapis_com.job.pubsub.write_latencies', 'cloud.gcp.dataflow_googleapis_com.job.system_lag', 'cloud.gcp.dataflow_googleapis_com.job.total_memory_usage_time', 'cloud.gcp.dataflow_googleapis_com.job.total_pd_usage_time', 'cloud.gcp.dataflow_googleapis_com.job.total_shuffle_data_processed', 'cloud.gcp.dataflow_googleapis_com.job.total_streaming_data_processed', 'cloud.gcp.dataflow_googleapis_com.job.total_vcpu_time', 'cloud.gcp.dataflow_googleapis_com.job.user_counter', 'cloud.gcp.dataproc_googleapis_com.cluster.hdfs.datanodes', 'cloud.gcp.dataproc_googleapis_com.cluster.hdfs.storage_capacity', 'cloud.gcp.dataproc_googleapis_com.cluster.hdfs.storage_utilization', 'cloud.gcp.dataproc_googleapis_com.cluster.hdfs.unhealthy_blocks', 'cloud.gcp.dataproc_googleapis_com.cluster.job.completion_time', 'cloud.gcp.dataproc_googleapis_com.cluster.job.duration', 'cloud.gcp.dataproc_googleapis_com.cluster.job.failed_count', 'cloud.gcp.dataproc_googleapis_com.cluster.job.running_count.gauge', 'cloud.gcp.dataproc_googleapis_com.cluster.job.submitted_count', 'cloud.gcp.dataproc_googleapis_com.cluster.operation.completion_time', 'cloud.gcp.dataproc_googleapis_com.cluster.operation.duration', 'cloud.gcp.dataproc_googleapis_com.cluster.operation.failed_count', 'cloud.gcp.dataproc_googleapis_com.cluster.operation.running_count.gauge', 'cloud.gcp.dataproc_googleapis_com.cluster.operation.submitted_count', 'cloud.gcp.dataproc_googleapis_com.cluster.yarn.allocated_memory_percentage', 'cloud.gcp.dataproc_googleapis_com.cluster.yarn.apps', 'cloud.gcp.dataproc_googleapis_com.cluster.yarn.containers', 'cloud.gcp.dataproc_googleapis_com.cluster.yarn.memory_size', 'cloud.gcp.dataproc_googleapis_com.cluster.yarn.nodemanagers', 'cloud.gcp.dataproc_googleapis_com.cluster.yarn.pending_memory_size', 'cloud.gcp.dataproc_googleapis_com.cluster.yarn.virtual_cores', 'cloud.gcp.datastore_googleapis_com.api.request_count', 'cloud.gcp.datastore_googleapis_com.entity.read_sizes', 'cloud.gcp.datastore_googleapis_com.entity.write_sizes', 'cloud.gcp.datastore_googleapis_com.index.write_count', 'cloud.gcp.dns_googleapis_com.query.response_count', 'cloud.gcp.file_googleapis_com.nfs.server.average_read_latency', 'cloud.gcp.file_googleapis_com.nfs.server.average_write_latency', 'cloud.gcp.file_googleapis_com.nfs.server.free_bytes', 'cloud.gcp.file_googleapis_com.nfs.server.free_bytes_percent', 'cloud.gcp.file_googleapis_com.nfs.server.metadata_ops_count', 'cloud.gcp.file_googleapis_com.nfs.server.procedure_call_count', 'cloud.gcp.file_googleapis_com.nfs.server.read_bytes_count', 'cloud.gcp.file_googleapis_com.nfs.server.read_milliseconds_count', 'cloud.gcp.file_googleapis_com.nfs.server.read_ops_count', 'cloud.gcp.file_googleapis_com.nfs.server.used_bytes', 'cloud.gcp.file_googleapis_com.nfs.server.used_bytes_percent', 'cloud.gcp.file_googleapis_com.nfs.server.write_bytes_count', 'cloud.gcp.file_googleapis_com.nfs.server.write_milliseconds_count', 'cloud.gcp.file_googleapis_com.nfs.server.write_ops_count', 'cloud.gcp.firebasestorage_googleapis_com.rules.evaluation_count', 'cloud.gcp.firestore_googleapis_com.api.request_count', 'cloud.gcp.firestore_googleapis_com.document.read_count', 'cloud.gcp.firestore_googleapis_com.document.write_count', 'cloud.gcp.firestore_googleapis_com.network.active_connections', 'cloud.gcp.firestore_googleapis_com.network.snapshot_listeners', 'cloud.gcp.firestore_googleapis_com.rules.evaluation_count', 'cloud.gcp.interconnect_googleapis_com.network.attachment.capacity', 'cloud.gcp.interconnect_googleapis_com.network.attachment.received_bytes_count', 'cloud.gcp.interconnect_googleapis_com.network.attachment.received_packets_count', 'cloud.gcp.interconnect_googleapis_com.network.attachment.sent_bytes_count', 'cloud.gcp.interconnect_googleapis_com.network.attachment.sent_packets_count', 'cloud.gcp.interconnect_googleapis_com.network.interconnect.capacity', 'cloud.gcp.interconnect_googleapis_com.network.interconnect.link.operational', 'cloud.gcp.interconnect_googleapis_com.network.interconnect.link.rx_power', 'cloud.gcp.interconnect_googleapis_com.network.interconnect.link.tx_power', 'cloud.gcp.interconnect_googleapis_com.network.interconnect.operational', 'cloud.gcp.interconnect_googleapis_com.network.interconnect.received_bytes_count', 'cloud.gcp.interconnect_googleapis_com.network.interconnect.received_unicast_packets_count', 'cloud.gcp.interconnect_googleapis_com.network.interconnect.sent_bytes_count', 'cloud.gcp.interconnect_googleapis_com.network.interconnect.sent_unicast_packets_count', 'cloud.gcp.kubernetes_io.node_daemon.cpu.core_usage_time.count', 'cloud.gcp.kubernetes_io.node_daemon.memory.used_bytes', 'cloud.gcp.kubernetes_io.node.cpu.allocatable_cores', 'cloud.gcp.kubernetes_io.node.cpu.allocatable_utilization', 'cloud.gcp.kubernetes_io.node.cpu.core_usage_time.count', 'cloud.gcp.kubernetes_io.node.cpu.total_cores', 'cloud.gcp.kubernetes_io.node.ephemeral_storage.allocatable_bytes', 'cloud.gcp.kubernetes_io.node.ephemeral_storage.inodes_free', 'cloud.gcp.kubernetes_io.node.ephemeral_storage.inodes_total', 'cloud.gcp.kubernetes_io.node.ephemeral_storage.total_bytes', 'cloud.gcp.kubernetes_io.node.ephemeral_storage.used_bytes', 'cloud.gcp.kubernetes_io.node.memory.allocatable_bytes', 'cloud.gcp.kubernetes_io.node.memory.allocatable_utilization', 'cloud.gcp.kubernetes_io.node.memory.total_bytes', 'cloud.gcp.kubernetes_io.node.memory.used_bytes', 'cloud.gcp.kubernetes_io.node.network.received_bytes_count', 'cloud.gcp.kubernetes_io.node.network.sent_bytes_count', 'cloud.gcp.kubernetes_io.node.pid_limit', 'cloud.gcp.kubernetes_io.node.pid_used', 'cloud.gcp.loadbalancing_googleapis_com.https.backend_latencies', 'cloud.gcp.loadbalancing_googleapis_com.https.backend_request_bytes_count', 'cloud.gcp.loadbalancing_googleapis_com.https.backend_request_count', 'cloud.gcp.loadbalancing_googleapis_com.https.backend_response_bytes_count', 'cloud.gcp.loadbalancing_googleapis_com.https.frontend_tcp_rtt', 'cloud.gcp.loadbalancing_googleapis_com.https.request_bytes_count', 'cloud.gcp.loadbalancing_googleapis_com.https.request_count', 'cloud.gcp.loadbalancing_googleapis_com.https.response_bytes_count', 'cloud.gcp.loadbalancing_googleapis_com.https.total_latencies', 'cloud.gcp.loadbalancing_googleapis_com.l3.external.egress_bytes_count', 'cloud.gcp.loadbalancing_googleapis_com.l3.external.egress_packets_count', 'cloud.gcp.loadbalancing_googleapis_com.l3.external.ingress_bytes_count', 'cloud.gcp.loadbalancing_googleapis_com.l3.external.ingress_packets_count', 'cloud.gcp.loadbalancing_googleapis_com.l3.external.rtt_latencies', 'cloud.gcp.loadbalancing_googleapis_com.l3.internal.egress_bytes_count', 'cloud.gcp.loadbalancing_googleapis_com.l3.internal.egress_packets_count', 'cloud.gcp.loadbalancing_googleapis_com.l3.internal.ingress_bytes_count', 'cloud.gcp.loadbalancing_googleapis_com.l3.internal.ingress_packets_count', 'cloud.gcp.loadbalancing_googleapis_com.l3.internal.rtt_latencies', 'cloud.gcp.logging_googleapis_com.exports.byte_count', 'cloud.gcp.logging_googleapis_com.exports.error_count', 'cloud.gcp.logging_googleapis_com.exports.log_entry_count', 'cloud.gcp.logging.googleapis.com.log_entry_count', 'cloud.gcp.managedidentities_googleapis_com.microsoft_ad.domain.health', 'cloud.gcp.ml_googleapis_com.prediction.online.cpu.utilization', 'cloud.gcp.ml_googleapis_com.prediction.online.memory.bytes_used', 'cloud.gcp.ml_googleapis_com.prediction.online.network.bytes_received.count', 'cloud.gcp.ml_googleapis_com.prediction.online.network.bytes_sent.count', 'cloud.gcp.ml_googleapis_com.prediction.online.replicas', 'cloud.gcp.ml_googleapis_com.prediction.online.target_replicas', 'cloud.gcp.ml_googleapis_com.training.cpu.utilization', 'cloud.gcp.ml_googleapis_com.training.memory.utilization', 'cloud.gcp.ml_googleapis_com.training.network.received_bytes_count', 'cloud.gcp.ml_googleapis_com.training.network.sent_bytes_count', 'cloud.gcp.monitoring_googleapis_com.uptime_check.check_passed', 'cloud.gcp.monitoring_googleapis_com.uptime_check.content_mismatch', 'cloud.gcp.monitoring_googleapis_com.uptime_check.request_latency', 'cloud.gcp.monitoring_googleapis_com.uptime_check.time_until_ssl_cert_expires', 'cloud.gcp.networking_googleapis_com.cloud_netslo.active_probing.probe_count', 'cloud.gcp.networking_googleapis_com.vm_flow.egress_bytes_count', 'cloud.gcp.networking_googleapis_com.vm_flow.ingress_bytes_count', 'cloud.gcp.networking_googleapis_com.vm_flow.rtt', 'cloud.gcp.networksecurity_googleapis_com.https.previewed_request_count', 'cloud.gcp.networksecurity_googleapis_com.https.request_count', 'cloud.gcp.pubsub_googleapis_com.subscription.ack_message_count', 'cloud.gcp.pubsub_googleapis_com.subscription.backlog_bytes', 'cloud.gcp.pubsub_googleapis_com.subscription.byte_cost.count', 'cloud.gcp.pubsub_googleapis_com.subscription.config_updates_count', 'cloud.gcp.pubsub_googleapis_com.subscription.dead_letter_message_count', 'cloud.gcp.pubsub_googleapis_com.subscription.mod_ack_deadline_message_count', 'cloud.gcp.pubsub_googleapis_com.subscription.mod_ack_deadline_message_operation_count', 'cloud.gcp.pubsub_googleapis_com.subscription.mod_ack_deadline_request_count', 'cloud.gcp.pubsub_googleapis_com.subscription.num_outstanding_messages', 'cloud.gcp.pubsub_googleapis_com.subscription.num_retained_acked_messages', 'cloud.gcp.pubsub_googleapis_com.subscription.num_retained_acked_messages_by_region', 'cloud.gcp.pubsub_googleapis_com.subscription.num_unacked_messages_by_region', 'cloud.gcp.pubsub_googleapis_com.subscription.num_undelivered_messages', 'cloud.gcp.pubsub_googleapis_com.subscription.oldest_retained_acked_message_age', 'cloud.gcp.pubsub_googleapis_com.subscription.oldest_retained_acked_message_age_by_region', 'cloud.gcp.pubsub_googleapis_com.subscription.oldest_unacked_message_age', 'cloud.gcp.pubsub_googleapis_com.subscription.oldest_unacked_message_age_by_region', 'cloud.gcp.pubsub_googleapis_com.subscription.pull_ack_message_operation_count', 'cloud.gcp.pubsub_googleapis_com.subscription.pull_ack_request_count', 'cloud.gcp.pubsub_googleapis_com.subscription.pull_message_operation_count', 'cloud.gcp.pubsub_googleapis_com.subscription.pull_request_count', 'cloud.gcp.pubsub_googleapis_com.subscription.push_request_count', 'cloud.gcp.pubsub_googleapis_com.subscription.push_request_latencies', 'cloud.gcp.pubsub_googleapis_com.subscription.retained_acked_bytes', 'cloud.gcp.pubsub_googleapis_com.subscription.retained_acked_bytes_by_region', 'cloud.gcp.pubsub_googleapis_com.subscription.sent_message_count', 'cloud.gcp.pubsub_googleapis_com.subscription.streaming_pull_message_operation_count', 'cloud.gcp.pubsub_googleapis_com.subscription.streaming_pull_mod_ack_deadline_message_operation_count', 'cloud.gcp.pubsub_googleapis_com.subscription.streaming_pull_mod_ack_deadline_request_count', 'cloud.gcp.pubsub_googleapis_com.subscription.streaming_pull_response_count', 'cloud.gcp.pubsub_googleapis_com.subscription.unacked_bytes_by_region', 'cloud.gcp.pubsub_googleapis_com.topic.byte_cost.count', 'cloud.gcp.pubsub_googleapis_com.topic.config_updates_count', 'cloud.gcp.pubsub_googleapis_com.topic.message_sizes', 'cloud.gcp.pubsub_googleapis_com.topic.num_retained_acked_messages_by_region', 'cloud.gcp.pubsub_googleapis_com.topic.num_unacked_messages_by_region', 'cloud.gcp.pubsub_googleapis_com.topic.oldest_retained_acked_message_age_by_region', 'cloud.gcp.pubsub_googleapis_com.topic.oldest_unacked_message_age_by_region', 'cloud.gcp.pubsub_googleapis_com.topic.retained_acked_bytes_by_region', 'cloud.gcp.pubsub_googleapis_com.topic.send_message_operation_count', 'cloud.gcp.pubsub_googleapis_com.topic.send_request_count', 'cloud.gcp.pubsub_googleapis_com.topic.unacked_bytes_by_region', 'cloud.gcp.redis_googleapis_com.clients.blocked', 'cloud.gcp.redis_googleapis_com.clients.connected', 'cloud.gcp.redis_googleapis_com.commands.calls.count', 'cloud.gcp.redis_googleapis_com.commands.total_time.count', 'cloud.gcp.redis_googleapis_com.commands.usec_per_call', 'cloud.gcp.redis_googleapis_com.keyspace.avg_ttl', 'cloud.gcp.redis_googleapis_com.keyspace.keys', 'cloud.gcp.redis_googleapis_com.keyspace.keys_with_expiration', 'cloud.gcp.redis_googleapis_com.persistence.rdb.bgsave_in_progress', 'cloud.gcp.redis_googleapis_com.replication.master_repl_offset', 'cloud.gcp.redis_googleapis_com.replication.master.slaves.lag', 'cloud.gcp.redis_googleapis_com.replication.master.slaves.offset', 'cloud.gcp.redis_googleapis_com.replication.offset_diff', 'cloud.gcp.redis_googleapis_com.replication.role', 'cloud.gcp.redis_googleapis_com.server.uptime', 'cloud.gcp.redis_googleapis_com.stats.cache_hit_ratio', 'cloud.gcp.redis_googleapis_com.stats.connections.total.count', 'cloud.gcp.redis_googleapis_com.stats.cpu_utilization.count', 'cloud.gcp.redis_googleapis_com.stats.evicted_keys.count', 'cloud.gcp.redis_googleapis_com.stats.expired_keys.count', 'cloud.gcp.redis_googleapis_com.stats.keyspace_hits.count', 'cloud.gcp.redis_googleapis_com.stats.keyspace_misses.count', 'cloud.gcp.redis_googleapis_com.stats.memory.maxmemory', 'cloud.gcp.redis_googleapis_com.stats.memory.system_memory_overload_duration.count', 'cloud.gcp.redis_googleapis_com.stats.memory.system_memory_usage_ratio', 'cloud.gcp.redis_googleapis_com.stats.memory.usage', 'cloud.gcp.redis_googleapis_com.stats.memory.usage_ratio', 'cloud.gcp.redis_googleapis_com.stats.network_traffic.count', 'cloud.gcp.redis_googleapis_com.stats.pubsub.channels', 'cloud.gcp.redis_googleapis_com.stats.pubsub.patterns', 'cloud.gcp.redis_googleapis_com.stats.reject_connections_count', 'cloud.gcp.router_googleapis_com.best_received_routes_count.gauge', 'cloud.gcp.router_googleapis_com.bgp_sessions_down_count.gauge', 'cloud.gcp.router_googleapis_com.bgp_sessions_up_count.gauge', 'cloud.gcp.router_googleapis_com.bgp.received_routes_count.gauge', 'cloud.gcp.router_googleapis_com.bgp.sent_routes_count.gauge', 'cloud.gcp.router_googleapis_com.bgp.session_up', 'cloud.gcp.router_googleapis_com.nat.allocated_ports', 'cloud.gcp.router_googleapis_com.nat.closed_connections_count', 'cloud.gcp.router_googleapis_com.nat.dropped_received_packets_count', 'cloud.gcp.router_googleapis_com.nat.dropped_sent_packets_count', 'cloud.gcp.router_googleapis_com.nat.nat_allocation_failed', 'cloud.gcp.router_googleapis_com.nat.new_connections_count', 'cloud.gcp.router_googleapis_com.nat.open_connections', 'cloud.gcp.router_googleapis_com.nat.port_usage', 'cloud.gcp.router_googleapis_com.nat.received_bytes_count', 'cloud.gcp.router_googleapis_com.nat.received_packets_count', 'cloud.gcp.router_googleapis_com.nat.sent_bytes_count', 'cloud.gcp.router_googleapis_com.nat.sent_packets_count', 'cloud.gcp.router_googleapis_com.router_up', 'cloud.gcp.router_googleapis_com.sent_routes_count.gauge', 'cloud.gcp.run_googleapis_com.container.billable_instance_time.count', 'cloud.gcp.run_googleapis_com.container.cpu.allocation_time.count', 'cloud.gcp.run_googleapis_com.container.cpu.utilizations', 'cloud.gcp.run_googleapis_com.container.instance_count.gauge', 'cloud.gcp.run_googleapis_com.container.max_request_concurrencies', 'cloud.gcp.run_googleapis_com.container.memory.allocation_time.count', 'cloud.gcp.run_googleapis_com.container.memory.utilizations', 'cloud.gcp.run_googleapis_com.container.network.received_bytes_count', 'cloud.gcp.run_googleapis_com.container.network.sent_bytes_count', 'cloud.gcp.run_googleapis_com.request_count', 'cloud.gcp.run_googleapis_com.request_latencies', 'cloud.gcp.serviceruntime_googleapis_com.api.request_count', 'cloud.gcp.serviceruntime_googleapis_com.api.request_latencies', 'cloud.gcp.serviceruntime_googleapis_com.api.request_sizes', 'cloud.gcp.serviceruntime_googleapis_com.api.response_sizes', 'cloud.gcp.serviceruntime_googleapis_com.quota.allocation.usage', 'cloud.gcp.serviceruntime_googleapis_com.quota.exceeded', 'cloud.gcp.serviceruntime_googleapis_com.quota.limit', 'cloud.gcp.serviceruntime_googleapis_com.quota.rate.net_usage.count', 'cloud.gcp.spanner_googleapis_com.api.api_request_count', 'cloud.gcp.spanner_googleapis_com.api.received_bytes_count', 'cloud.gcp.spanner_googleapis_com.api.request_count.gauge', 'cloud.gcp.spanner_googleapis_com.api.request_latencies', 'cloud.gcp.spanner_googleapis_com.api.sent_bytes_count', 'cloud.gcp.spanner_googleapis_com.instance.cpu.smoothed_utilization', 'cloud.gcp.spanner_googleapis_com.instance.cpu.utilization', 'cloud.gcp.spanner_googleapis_com.instance.cpu.utilization_by_priority', 'cloud.gcp.spanner_googleapis_com.instance.node_count.gauge', 'cloud.gcp.spanner_googleapis_com.instance.session_count.gauge', 'cloud.gcp.spanner_googleapis_com.instance.storage.limit_bytes', 'cloud.gcp.spanner_googleapis_com.instance.storage.used_bytes', 'cloud.gcp.spanner_googleapis_com.instance.storage.utilization', 'cloud.gcp.spanner_googleapis_com.query_count', 'cloud.gcp.storage_googleapis_com.api.request_count', 'cloud.gcp.storage_googleapis_com.authn.authentication_count', 'cloud.gcp.storage_googleapis_com.authz.acl_based_object_access_count', 'cloud.gcp.storage_googleapis_com.authz.acl_operations_count', 'cloud.gcp.storage_googleapis_com.authz.object_specific_acl_mutation_count', 'cloud.gcp.storage_googleapis_com.network.received_bytes_count', 'cloud.gcp.storage_googleapis_com.network.sent_bytes_count', 'cloud.gcp.storage_googleapis_com.storage.object_count.gauge', 'cloud.gcp.storage_googleapis_com.storage.total_byte_seconds', 'cloud.gcp.storage_googleapis_com.storage.total_bytes', 'cloud.gcp.vpcaccess_googleapis_com.connector.cpu.utilizations', 'cloud.gcp.vpcaccess_googleapis_com.connector.instances', 'cloud.gcp.vpcaccess_googleapis_com.connector.received_bytes_count', 'cloud.gcp.vpcaccess_googleapis_com.connector.received_packets_count', 'cloud.gcp.vpcaccess_googleapis_com.connector.sent_bytes_count', 'cloud.gcp.vpcaccess_googleapis_com.connector.sent_packets_count', 'cloud.gcp.vpn_googleapis_com.gateway.connections', 'cloud.gcp.vpn_googleapis_com.network.dropped_received_packets_count', 'cloud.gcp.vpn_googleapis_com.network.dropped_sent_packets_count', 'cloud.gcp.vpn_googleapis_com.network.received_bytes_count', 'cloud.gcp.vpn_googleapis_com.network.received_packets_count', 'cloud.gcp.vpn_googleapis_com.network.sent_bytes_count', 'cloud.gcp.vpn_googleapis_com.network.sent_packets_count', 'cloud.gcp.vpn_googleapis_com.tunnel_established']
#LIST=['cloud.gcp.agent_googleapis_com.agent.gae_app.api_request_count']
TENANT_ID='xxxx'
POLICY_ID='abcdefg-12345-abcd-1234-abcd'
##################################
## Variables
##################################
UG={}   
API_ACCOUNT='https://api.dynatrace.com/iam/v1/accounts/'
API_BINDING='https://api.dynatrace.com/iam/v1/repo/account/'
API_BINDING_ENV='https://api.dynatrace.com/iam/v1/repo/environment/'
wait=0.1

MZ_DIC={}
ENV_DIC={}
GROUPS_DIC={}
USERS_DIC={}
PREFIX=[]

#disable warning
urllib3.disable_warnings()


##################################
## Generic Dynatrace API
##################################

# generic function GET to call API with a given uri
def queryDynatraceAPI(uri,TOKEN):
    head = {
    'Accept': 'application/json',
    'Authorization': 'Bearer '+TOKEN
    }
    jsonContent = None
    response = requests.get(uri,headers=head,verify=False)
    # For successful API call, response code will be 200 (OK)
    if(response.ok):
        if(len(response.text) > 0):
            jsonContent = json.loads(response.text)
    else:
        jsonContent = json.loads(response.text)
        print(jsonContent)
        errorMessage = ""
        if(jsonContent["error"]):
            errorMessage = jsonContent["error"]["message"]
            print("Dynatrace API returned an error: " + errorMessage)
        #jsonContent = None
        raise Exception("Error", "Dynatrace API returned an error: " + errorMessage)

    return(jsonContent)

#generic function POST to call API with a given uri
def postDynatraceAPI(uri,payload,TOKEN):
    head = {
    'Accept': 'application/json',
    'Authorization': 'Bearer '+TOKEN
    }
    jsonContent = None
    response = requests.post(uri,headers=head,verify=False, json=payload)
    #print(response.text)
    # For  API call, response code will be 200 (OK)
    if(response.ok):
        if(len(response.text) > 0):
            try:
                jsonContent = json.loads(response.text)
            except:
                jsonContent = response.text
    else:
        jsonContent = json.loads(response.text)
        print(jsonContent)
        errorMessage = ""
        if(jsonContent["error"]):
            errorMessage = jsonContent["error"]["message"]
            print("Dynatrace API returned an error: " + errorMessage)
        #jsonContent = None
        raise Exception("Error", "Dynatrace API returned an error: " + errorMessage)

    return(jsonContent)

#generic function PUT to call API with a given uri
def putDynatraceAPI(uri, payload,TOKEN):
    head = {
    'Accept': 'application/json',
    'Authorization': 'Bearer '+TOKEN
    }
    jsonContent = None
    response = requests.put(uri,headers=head,verify=False, json=payload)
    # For successful API call, response code will be 200 (OK)
    if(response.ok):
        if(len(response.text) > 0):
            jsonContent = json.loads(response.text)
        jsonContent='success'
    else:
        jsonContent = json.loads(response.text)
        print(jsonContent)
        errorMessage = ""
        if(jsonContent["error"]):
            errorMessage = jsonContent["error"]["message"]
            print("Dynatrace API returned an error: " + errorMessage)
        #jsonContent = None
        raise Exception("Error", "Dynatrace API returned an error: " + errorMessage)

    return(jsonContent)


#generic function delete to call API with a given uri
def delDynatraceAPI(uri,TOKEN):
    head = {
    'Accept': 'application/json',
    'Authorization': 'Bearer '+TOKEN
    }
    jsonContent = None
    response = requests.delete(uri,headers=head,verify=False)
    # For successful API call, response code will be 200 (OK)
    if(response.ok):
        if(len(response.text) > 0):
            jsonContent = json.loads(response.text)
        jsonContent='success'
    else:
        jsonContent = json.loads(response.text)
        print(jsonContent)
        errorMessage = ""
        if(jsonContent["error"]):
            errorMessage = jsonContent["error"]["message"]
            print("Dynatrace API returned an error: " + errorMessage)
        #jsonContent = None
        raise Exception("Error", "Dynatrace API returned an error: " + errorMessage)

    return(jsonContent)

##################################
## IAM token
##################################
def iam_token():

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    scope='account-idm-write account-idm-read account-env-read account-env-write iam-policies-management iam:policies:write iam:policies:read iam:bindings:write iam:bindings:read iam:effective-permissions:read'
    #scope='iam-policies-management iam:policies:write iam:policies:read iam:bindings:write iam:bindings:read'
    r = requests.post(SSO_Endpoint+'?grant_type=client_credentials&client_id='+Client_ID+'&client_secret='+Client_Secret+'&resource='+Account_Urn+'&scope='+scope,headers=headers)
    #print(r.json())
    return(r.json()['access_token'])

##################################
## IAM token
##################################
def list_groups(CLIENT_ID,TOKEN):

    uri=API_ACCOUNT+CLIENT_ID+'/groups'

    datastore = queryDynatraceAPI(uri,TOKEN)
    #print(datastore)
    if datastore != []:
        for group in datastore['items']:
            if group['name'].startswith('cloud.gcp') :
                UG[group['name']]=group['uuid']
        
    return ()

##################################
## Create User GROUP
##################################
def create_group(CLIENT_ID,TOKEN,ugname):

    payload=[{
            "name": ugname,
            "description": "created by pipeline",
            "owner": "LOCAL"
            }]

    uri=API_ACCOUNT+CLIENT_ID+'/groups'
    result = postDynatraceAPI(uri,payload,TOKEN)
    UG[ugname]=result[0]['uuid']

    print(' => create user group: '+ugname)
        
    return (result)

##################################
## Mapp Policy with User GROUP
##################################
def binding_ug(CLIENT_ID,TOKEN,ugid,name):

    uri=API_BINDING_ENV+TENANT_ID+'/bindings/'+POLICY_ID+'/'+ugid
    payload={ 
              "parameters": { 
              "name": name 
              }
            }
    result = postDynatraceAPI(uri,payload,TOKEN)


    print(' => binding ug: '+ugid+' with key =  '+name)
        
    return (result)


##################################
## Main program
##################################
IAM_Token=iam_token()
list_groups(AccountUiid,IAM_Token)
for key in LIST:
 name=key.split('_')[0]
 if name not in PREFIX :
     PREFIX.append(name)
#print(UG)

'''
#create UG if not exists
for name in PREFIX:
 if name not in UG: 
    create_group(AccountUiid,IAM_Token,name)
    time.sleep(wait)
    
IAM_Token=iam_token()    
#bind UG
for name in PREFIX:
    binding_ug(AccountUiid,IAM_Token,UG[name],name)
'''

#verif
for ug in UG:
    print(ug)
    uri=API_BINDING_ENV+TENANT_ID+'/bindings/'+POLICY_ID+'/'+UG[ug]
    result = queryDynatraceAPI(uri,IAM_Token)
    print(result['policyBindings'])
'''

#delete UG
for ug in UG :
    print('delete', ug)
    uri=API_ACCOUNT+AccountUiid+'/groups/'+UG[ug]
    delDynatraceAPI(uri,IAM_Token)
'''

print("###")
