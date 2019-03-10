#!/usr/bin/env bash
#
# Author: A-Lang, created by 2019/2/28
# Purpose: Sends a push message to a user through LINE Messaging API.
#


# LINE APT Access Credentials
ChannelAccessToken='ChannelAccessToken'

Usage() { 
    echo "Usage: $0 [-t <TEXT-Message>] [-u <uid-or-gid>]"; 
    echo "For example: $0 -t \"Hello, SuperMan\" -u \"C2sh6dyg9sw4h772j8jw\" "
}

Check_cmd() {
    cmd="$1"
    if ! (which $cmd > /dev/null) ; then
        echo "The command $cmd Not Found !"
        return 1
    fi
    return 0
}

Emoji() {
    code=$(echo $1 | sed "s/\(..\)/\\\x\1/g")
    converted=$(echo -ne "\x0$code" | iconv -f UTF-32BE -t UTF-8)
    echo "$converted"
}

PushMsg() {
    api_url="https://api.line.me/v2/bot/message/push"
    post_txt="$(echo $1 | sed 's/\"//g')"  # remove the double-quote if it exists
    post_to="$2"

    json_data="{
        \"to\":\"$post_to\",
        \"messages\":[
            {
                \"type\":\"text\",
                \"text\":\"$(Emoji "10007B") $post_txt\"
            }
        ]
    }"

    http_response=$( echo $json_data | curl -v POST \
    -H "Content-Type:application/json" \
    -H "Authorization: Bearer $ChannelAccessToken" \
    -d @- "$api_url" )

}

while getopts ":t:u:" o; do
    case "$o" in
        t)
            t=$OPTARG
            ;;
        u)
            u=$OPTARG
            ;;
        \?)
            echo "Invalid option: -$OPTARG"
            Usage
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument !"
            Usage
            exit 1
            ;;
    esac
done

if [ $OPTIND -ne 5 ]; then
    echo "Invalid options entered !"
    Usage
    exit 1
fi

txt="$t"
to="$u"

# Check the commands required
Check_cmd "curl" || exit 1
Check_cmd "iconv" || exit 1

# Sending a push message
PushMsg "$txt" "$to"

[ -n "$http_response" ] && echo "HTTP Response: $http_response"