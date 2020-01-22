compctl -K _passes -x 's[--]' -k '(all atv vodafone)' --  passes

_passes() {
  local completions

  completions="$(passes --list_users)"

  reply=(${(ps:\n:)completions})
}
