#/usr/bin/env sh
ssh -i ~/.ssh/hackOregonServerKey.pem ubuntu@54.213.83.132 'sudo -u postgres pg_dump hackoregon | nice -n 20 gzip -9 > hackoregon_dump_2015-10-02.gz'
scp -i ~/.ssh/hackOregonServerKey.pem ubuntu@54.213.83.132:hackoregon_dump_2015-10-02.gz .