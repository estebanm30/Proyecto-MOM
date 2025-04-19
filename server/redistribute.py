from controllers.queue_controller import redistribute_queue
from server.zookeeper import get_all_queues, get_servers
from server.zookeeper import get_queues_handled_by


def redistribute_q(rq):
    all_queues = get_all_queues()
    alive_servers = get_servers()
    servers_queues = {}

    for server in alive_servers:
        server_queues = get_queues_handled_by(server)
        servers_queues[server] = server_queues

    for queue in rq:
        is_replica = queue.endswith("_replica")
        base_name = queue[:-8] if is_replica else queue

        for candidate_server in alive_servers:
            assigned_queues = server_queues[candidate_server]

            if is_replica and base_name in assigned_queues:
                continue
            if not is_replica and f"{base_name}_replica" in assigned_queues:
                continue
            
            redistribute_queue(candidate_server, queue)
            print(f"Redistribuida '{queue}' a {candidate_server}")
            break