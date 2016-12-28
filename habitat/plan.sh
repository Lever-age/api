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
  # This hack deals with some npm package build scripts having
  # /usr/bin/env hardcoded instead of using env from PATH by
  # temporarily creating a symlink at /usr/bin/env within
  # the build environment that links to the env executable
  # provided by the coreutils package
  #
  # Habitat provides a minimal environment for builds where every
  # available package has its bin folder added to PATH rather than
  # its contents copied to a global /usr/bin directory

  if [[ ! -r /usr/bin/env ]]; then
    ln -sv "$(pkg_path_for coreutils)/bin/env" /usr/bin/env
    _clean_env=true
  fi
}

do_build() {
  # Copy files from wherever this plan is being run from to the
  # temporary build space for this package
  cp -vr $PLAN_CONTEXT/../* $HAB_CACHE_SRC_PATH/$pkg_dirname

  # cd into the temporary build space and populate node_modules/
  cd $HAB_CACHE_SRC_PATH/$pkg_dirname
  npm install
}

do_install() {
  # Copy the things we want to distribute from the current
  # directory (this package's temporary build space) to the
  # root for this package's build
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
