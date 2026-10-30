#!/bin/bash
# Incremental knowledge tarballs. Does not rebuild original wheel/deb releases.
# Excludes _local_only, docs_html, and NC / personal-use vendor archives.
set -euo pipefail
LIB=/root/engineering_offline_library
OUT="$LIB/assets"
mkdir -p "$OUT"
STAMP=$(date -u +%Y%m%d)
cd /root

tar --format=pax --owner=0 --group=0 --numeric-owner \
  -C /root \
  -cf "$OUT/knowledge-guides-projects_${STAMP}.tar" \
  engineering_offline_library/README.md \
  engineering_offline_library/00_portal \
  engineering_offline_library/01_math \
  engineering_offline_library/02_signal \
  engineering_offline_library/03_control_estimation \
  engineering_offline_library/04_data_ai \
  engineering_offline_library/05_embedded_linux \
  engineering_offline_library/06_boards \
  engineering_offline_library/07_comms_iot \
  engineering_offline_library/08_robotics_uav \
  engineering_offline_library/09_engineering \
  engineering_offline_library/10_quant_finance \
  engineering_offline_library/projects \
  engineering_offline_library/scripts \
  engineering_offline_library/inventories \
  engineering_offline_library/.release_exclude

tar --format=pax --owner=0 --group=0 --numeric-owner \
  -C /root \
  --exclude='engineering_offline_library/vendor/pumpkin-book-master.tar.gz' \
  --exclude='engineering_offline_library/vendor/leedl-tutorial-master.tar.gz' \
  --exclude='engineering_offline_library/vendor/ThinkDSP-master.tar.gz' \
  --exclude='engineering_offline_library/vendor/underactuated-tedrake-master.tar.gz' \
  --exclude='engineering_offline_library/vendor/cvxbook_additional_exercises-main.tar.gz' \
  --exclude='engineering_offline_library/vendor/ardupilot_wiki-master.tar.gz' \
  --exclude='engineering_offline_library/vendor/PX4-user_guide-main.tar.gz' \
  --exclude='engineering_offline_library/vendor/raspberrypi-documentation-master.tar.gz' \
  -cf "$OUT/knowledge-public-vendor_${STAMP}.tar" \
  engineering_offline_library/_public \
  engineering_offline_library/vendor

tar --format=pax --owner=0 --group=0 --numeric-owner \
  -C /root \
  -cf "$OUT/knowledge-vendor-large-wikis_${STAMP}.tar" \
  engineering_offline_library/vendor/ardupilot_wiki-master.tar.gz \
  engineering_offline_library/vendor/PX4-user_guide-main.tar.gz \
  engineering_offline_library/vendor/raspberrypi-documentation-master.tar.gz

( cd "$OUT" && sha256sum \
  knowledge-guides-projects_${STAMP}.tar \
  knowledge-public-vendor_${STAMP}.tar \
  knowledge-vendor-large-wikis_${STAMP}.tar \
  > SHA256SUMS_${STAMP}.txt )
echo "wrote $OUT (local_only and NC vendor excluded)"
ls -lh "$OUT"
