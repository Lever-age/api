pkg_origin=leverage
pkg_name=leverage-api
pkg_version=0.1.0
pkg_maintainer="Chris Alfano <chris@codeforphilly.org>"
pkg_license=(MIT)
pkg_upstream_url=https://github.com/Lever-age/api
pkg_source=leverage-api.tar.gz
pkg_deps=(bochener/node)
pkg_expose=(8228)
pkg_build_deps=(core/coreutils)

do_download() {
  return 0
}

do_verify() {
  return 0
}

do_unpack() {
  return 0
}

do_prepare() {
  # The `/usr/bin/env` path is hardcoded, so we'll add a symlink if needed.
  # We can't do fix_interpreter here without adding a coreutils runtime dep.
  if [[ ! -r /usr/bin/env ]]; then
    ln -sv "$(pkg_path_for coreutils)/bin/env" /usr/bin/env
    _clean_env=true
  fi
}

do_build() {
  cp -vr $PLAN_CONTEXT/../* $HAB_CACHE_SRC_PATH/$pkg_dirname

  cd $HAB_CACHE_SRC_PATH/$pkg_dirname
  npm install
}

do_install() {
  # Our source files were copied over to HAB_CACHE_SRC_PATH/$pkg_dirname in do_build(),
  # and now they need to be copied from that directory into the root directory of our package
  # through the use of the pkg_prefix variable.

  cp -v package.json ${pkg_prefix}
  cp -v app.js ${pkg_prefix}
  cp -vr controllers ${pkg_prefix}
  cp -vr lib ${pkg_prefix}
  cp -r node_modules ${pkg_prefix}
}

do_end() {
  # Clean up the `env` link, if we set it up.
  if [[ -n "$_clean_env" ]]; then
    rm -fv /usr/bin/env
  fi
}
