# One line per thing said or run; tool output is left out. Usage: jq -r -f extract.jq <session>.jsonl
select(.type == "user" or .type == "assistant") | select(.isMeta | not)
| "\(.timestamp) \(.message.role)" as $who
| .message.content
| if type == "string" then "\($who): \(.)"
  else .[]
  | if .type == "text" then "\($who): \(.text)"
    elif .type == "tool_use" then "\($who) ran \(.name): \(.input.command // .input.file_path // .input.skill // .input.description // "")"
    else empty end
  end
