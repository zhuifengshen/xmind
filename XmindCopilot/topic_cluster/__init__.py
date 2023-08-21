from XmindCopilot.core.topic import TopicElement
from XmindCopilot.core.markerref import MarkerId
from XmindCopilot.search import topic_search
from .TextCluster.cluster import cluster, ClusterArgs


def topic_cluster(topic, recursive=False, seg_line_markerId=MarkerId.flagRed, args=ClusterArgs()):
    topic.removeSubTopicbyMarkerId(seg_line_markerId)
    topics = topic.getSubTopics()
    if recursive:
        for t in topics:
            topic_cluster(t, recursive, seg_line_markerId, args)
    if len(topics) > 1:
        # TODO: Multi-line title needs to be handled
        # (although it might not cause problems temporarily)
        namelist = [t.getTitle() for t in topics]
        cluster_result = cluster(args, namelist)
        for c in cluster_result:
            for title in c:
                if title:
                    t = topic_search(topic, title)
                    if t:
                        t.moveTopic(-1)
                    else:
                        print("failed to search:", title)
            tmptopic = TopicElement(ownerWorkbook=topic.getOwnerWorkbook(), title="———")
            tmptopic.addMarker(seg_line_markerId)
            topic.addSubTopic(tmptopic)


if __name__ == "__main__":
    # import numpy
    # data = cluster(args, ret_output=True)
    # print(data[0])
    pass
