import koji
import datetime
import time

session = koji.ClientSession('https://koji.fedoraproject.org/kojihub')
tags = session.listTags(package='module-build-macros')
now = time.mktime(datetime.datetime.utcnow().timetuple())
then = now - (1209600.0)

import random
random.shuffle(tags)
N = len(tags)
for i, tag in enumerate(tags):
    name = tag['name']
    if name.endswith('-build'):
        continue

    now = datetime.datetime.now().isoformat().split('T')[1]
    print "%s (%i of %i): %s" % (now, i, N, name)

    rpms = session.listTaggedRPMS(tag['id'])

    for entry in rpms:
        for rpm in entry:
            if not 'id' in rpm:
                continue
            result = session.queryRPMSigs(rpm_id=rpm['id'])
            if not result:
                print "FOUND UNSIGNED!  Writing to tags.txt", name
                with open('tags.txt', 'a') as f:
                    s = "{tag}, {name}-{version}-{release}\n".format(tag=name, **rpm)
                    f.write(s)
            break
