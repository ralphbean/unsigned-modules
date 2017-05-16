
import operator

import arrow
import requests

with open('tags.txt', 'r') as f:
    lines = f.readlines()

tags = [line.split(',')[0] for line in lines]

url = 'https://pdc.fedoraproject.org/rest_api/v1/unreleasedvariants/?koji_tag=%s'

details = {}
for tag in tags:
    print "Looking up %r" % tag
    response = requests.get(url % tag)
    data = response.json()
    assert data['count'] == 1, data
    details[tag] = data['results'][0]

details = sorted(details.values(), key=operator.itemgetter('variant_release'))
with open('details.txt', 'w') as f:
    for detail in details:
        release = detail['variant_release']
        timestamp = "%s-%s-%s %s:%s:%s" % (
            release[0:4], release[4:6], release[6:8],
            release[8:10], release[10:12], release[12:14],
        )
        f.write("{tag}, corresponding to {module}, built {ago}\n".format(
            tag=detail['koji_tag'],
            module=detail['variant_uid'],
            ago=arrow.get(timestamp).humanize(),
        ))
