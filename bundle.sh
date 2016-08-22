#!/bin/sh
GEMFILE="https://raw.githubusercontent.com/owner/repo/development/Gemfile?token=ACt0HIXk4-8Ilzz9O51AFdcgE475TPC-ks5XYZSFwA%3D%3D"
GEMFILE_LOCK="https://raw.githubusercontent.com/owner/repo/development/Gemfile.lock?token=ACt0HKaD_AvvACB4VXr3kAMM_TaESrNVks5XYZSHwA%3D%3D"
TMPDIR="/tmp/bungler"
RUBYROOT=`ls -d  /opt/rubies/ruby-[0-9]* | tail -1`
RUBYVER=`echo ${RUBYROOT} | cut -f2 -d"-"`
export RUBY_ROOT=${RUBYROOT}
export PATH=${RUBYROOT}/bin:/opt/elasticbeanstalk/lib/ruby/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/sbin:/sbin:/bin
export RUBY_ENGINE=ruby;
export RUBY_VERSION=${RUBYVER}
export GEM_ROOT=${RUBYROOT}/lib/ruby/gems/${RUBYVER}
echo "RUBYROOT: ${RUBYROOT}"
echo "PATH: ${PATH}"
echo "RUBY_ENGINE: ${RUBY_ENGINE}"
echo "RUBY_VERSION: ${RUBY_VERSION}"
echo "GEM_ROOT: ${GEM_ROOT}"

yum install -y ruby23-devel
mkdir ${TMPDIR} && cd ${TMPDIR}
curl ${GEMFILE} -o Gemfile
curl ${GEMFILE_LOCK} -o Gemfile.lock
gem install bundler
bundle install --without development test
bundle show teaspoon
#sleep 10000
cd / && rm -rf ${TMPDIR}
ls -al ${RUBYROOT}/lib/ruby/gems/${RUBYVER}
