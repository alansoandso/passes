compctl -K _passes -x 's[--]' -k '(all atv prod_user vodafone)' --  passes

_passes() {
  local completions

  completions="$(passes --list_users)"

  reply=(${(ps:\n:)completions})
}
