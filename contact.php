<?php
// エラーレポートを無効化（本番環境用）
error_reporting(0);
ini_set('display_errors', 0);

// レスポンスヘッダーを設定
header('Content-Type: application/json; charset=utf-8');

// セキュリティヘッダー
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('X-XSS-Protection: 1; mode=block');

// POSTメソッドのみ許可
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

// CSRFトークンのチェック（簡易版）
$allowed_referers = [
    'https://toshi776.com',
    'http://toshi776.com',
    'https://www.toshi776.com',
    'http://www.toshi776.com'
];

$referer = $_SERVER['HTTP_REFERER'] ?? '';
$is_valid_referer = false;
foreach ($allowed_referers as $allowed) {
    if (strpos($referer, $allowed) === 0) {
        $is_valid_referer = true;
        break;
    }
}

if (!$is_valid_referer) {
    http_response_code(403);
    echo json_encode(['success' => false, 'message' => 'Invalid referer']);
    exit;
}

// 入力値の取得とサニタイズ
$name = trim($_POST['name'] ?? '');
$email = trim($_POST['email'] ?? '');
$company = trim($_POST['company'] ?? '');
$subject = trim($_POST['subject'] ?? '');
$message = trim($_POST['message'] ?? '');

// バリデーション
$errors = [];

if (empty($name) || mb_strlen($name) > 50) {
    $errors[] = 'お名前は必須で、50文字以内で入力してください。';
}

if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL) || mb_strlen($email) > 100) {
    $errors[] = '有効なメールアドレスを入力してください。';
}

if (!empty($company) && mb_strlen($company) > 100) {
    $errors[] = '会社名は100文字以内で入力してください。';
}

if (empty($message) || mb_strlen($message) > 2000) {
    $errors[] = 'ご相談内容は必須で、2000文字以内で入力してください。';
}

// スパム対策：短時間での連続送信チェック
session_start();
$last_submit = $_SESSION['last_submit'] ?? 0;
$current_time = time();
if ($current_time - $last_submit < 60) {
    $errors[] = '送信間隔が短すぎます。1分後に再度お試しください。';
}

// エラーがある場合は返却
if (!empty($errors)) {
    echo json_encode(['success' => false, 'message' => implode('\n', $errors)]);
    exit;
}

// メール送信設定
$to = 'toshi776@gmail.com';
$mail_subject = '[イワシス:AI×DXコンサルティング] お問い合わせ: ' . $subject;

// メール本文作成
$mail_body = "イワシス：AI×DXコンサルティング お問い合わせフォームより\n\n";
$mail_body .= "■お名前\n{$name}\n\n";
$mail_body .= "■メールアドレス\n{$email}\n\n";
$mail_body .= "■会社名・組織名\n" . ($company ?: '未入力') . "\n\n";
$mail_body .= "■お問い合わせ種別\n" . ($subject ?: '未選択') . "\n\n";
$mail_body .= "■ご相談内容\n{$message}\n\n";
$mail_body .= "■送信日時\n" . date('Y-m-d H:i:s') . "\n\n";
$mail_body .= "■送信者IP\n" . $_SERVER['REMOTE_ADDR'] . "\n";
$mail_body .= "■User-Agent\n" . $_SERVER['HTTP_USER_AGENT'] . "\n";

// メールヘッダー設定
$headers = [];
$headers[] = 'From: noreply@toshi776.com';
$headers[] = 'Reply-To: ' . $email;
$headers[] = 'X-Mailer: PHP/' . phpversion();
$headers[] = 'Content-Type: text/plain; charset=UTF-8';

// メール送信
$mail_sent = mail($to, $mail_subject, $mail_body, implode("\r\n", $headers));

if ($mail_sent) {
    // 送信成功時の処理
    $_SESSION['last_submit'] = $current_time;
    
    // 自動返信メールも送信
    $auto_reply_subject = '[イワシス:AI×DXコンサルティング] お問い合わせありがとうございます';
    $auto_reply_body = "{$name} 様\n\n";
    $auto_reply_body .= "この度は イワシス：AI×DXコンサルティング にお問い合わせいただき、ありがとうございます。\n\n";
    $auto_reply_body .= "以下の内容でお問い合わせを受け付けいたしました。\n";
    $auto_reply_body .= "内容を確認の上、2営業日以内にご連絡いたします。\n\n";
    $auto_reply_body .= "【お問い合わせ内容】\n";
    $auto_reply_body .= "お名前: {$name}\n";
    $auto_reply_body .= "メールアドレス: {$email}\n";
    $auto_reply_body .= "会社名: " . ($company ?: '未入力') . "\n";
    $auto_reply_body .= "お問い合わせ種別: " . ($subject ?: '未選択') . "\n";
    $auto_reply_body .= "ご相談内容: {$message}\n\n";
    $auto_reply_body .= "お急ぎの場合は、以下のSNSからもご連絡いただけます。\n";
    $auto_reply_body .= "Twitter: @your_twitter\n";
    $auto_reply_body .= "LinkedIn: https://linkedin.com/in/your-profile\n\n";
    $auto_reply_body .= "今後ともよろしくお願いいたします。\n\n";
    $auto_reply_body .= "イワシス：AI×DXコンサルティング";
    
    $auto_reply_headers = [];
    $auto_reply_headers[] = 'From: イワシス：AI×DXコンサルティング <noreply@toshi776.com>';
    $auto_reply_headers[] = 'X-Mailer: PHP/' . phpversion();
    $auto_reply_headers[] = 'Content-Type: text/plain; charset=UTF-8';
    
    mail($email, $auto_reply_subject, $auto_reply_body, implode("\r\n", $auto_reply_headers));
    
    echo json_encode([
        'success' => true, 
        'message' => 'お問い合わせありがとうございます。内容を確認の上、2営業日以内にご連絡いたします。'
    ]);
} else {
    echo json_encode([
        'success' => false, 
        'message' => '送信に失敗しました。お手数ですが、再度お試しください。'
    ]);
}
?>