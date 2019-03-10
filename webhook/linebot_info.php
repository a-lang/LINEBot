<?php

/**
* Author : A-Lang, written by 2019/2/22
* Purpose: This Line Bot is used to get the userid/groupid for the Line user.
* Usage  : Once the Bot is added as a friend in your Line account, you can send
*          the follow txts to get some info.
*
*         /uid   ,return the info of your current Line userid
*         /gid   ,return the info of your current Line groupid
* 
*/

require_once('./LINEBotTiny.php');

// Channel Secret
$channelSecret = "ChannelSecret";

// Channel Access Token
$channelAccessToken = "ChannelAccessToken";

$http_header = array(
        'Content-Type: application/json',
        'Authorization: Bearer ' . $channelAccessToken
);

$client = new LINEBotTiny($channelAccessToken, $channelSecret);
foreach ($client->parseEvents() as $event) {
    // Uncomment the line below for debugging your codes
    file_put_contents("app_log", date("Y-m-d H:i:s") . " => \n" . json_encode($event));

    switch ($event['type']) {
        case 'message':
            $message = $event['message'];
            switch ($message['type']) {
                case 'text':
                    $uid = $event['source']['userId'];
                    if ($message['text'] === '/uid') {
                        reply('text', "您好 " . get_username($uid) . " " . emoji('100001') . "\r\n您的 Line 帳號內碼是 " . $uid);
                        //reply('text', emoji('100005'));
                    } elseif ($message['text'] === '/gid') {
                        $gid = $event['source']['groupId'];
                        if (!empty($gid)) {
                            reply('text', "您好 " . get_username($uid) . " " . emoji('100001') . "\r\n目前 Line 群組的內碼是 " . $gid);
                        } else {
                            reply('text', "您好 " . get_username($uid) . " " . emoji('10000E') . "\r\n查不到目前 Line 群組的內碼 ");
                        }
                    }
                    break;
            }
            break;

        default:
            error_log('Unsupported event type: ' . $event['type']);
            break;
    }
}

function reply($content_type, $message) {
    global $client, $event; 

    $client->replyMessage([
        'replyToken' => $event['replyToken'],
        'messages' => [
            [
                'type' => $content_type,
                'text' => $message
            ]
        ]
    ]);
}

function get_username($uid) {
    global $http_header;

    $url = 'https://api.line.me/v2/bot/profile/' . $uid;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HEADER,0);
	curl_setopt($ch, CURLOPT_HTTPHEADER, $http_header);
    $response = curl_exec($ch);
    //error_log('DEBUG: response => ' . $response);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    //error_log('DEBUG: http_code => ' . $http_code);
    curl_close($ch);

    if ($http_code == '200') {
        $string = json_decode($response, true);
        $username = $string['displayName'];
        return $username;
    }

    return NULL;
}

function emoji($code) {
    $bin = hex2bin(str_repeat('0', 8 - strlen($code)) . $code);
    $emoticon =  mb_convert_encoding($bin, 'UTF-8', 'UTF-32BE');
    return $emoticon;
}
