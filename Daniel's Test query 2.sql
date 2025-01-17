WITH Following AS(
SELECT DISTINCT flwee
FROM Follows
WHERE flwer == '97'
)
, FollowingTweets AS(
SELECT DISTINCT tid, writer, tdate, text
FROM Tweets
WHERE writer in Following
)
, FollowingRetweets AS(
SELECT DISTINCT t.tid, t.writer, r.rdate as tdate, t.text
FROM Tweets t, Retweets r
WHERE r.usr in Following
AND t.tid = r.tid
)
, Feed AS (
SELECT DISTINCT *
FROM FollowingTweets
UNION
SELECT DISTINCT *
FROM FollowingRetweets
)
SELECT
    ROW_NUMBER() OVER (ORDER BY f.tdate DESC) AS tweet_number, 
    f.tid,
    f.writer,
    r.usr,
    f.tdate, 
    f.text
FROM Feed f
LEFT JOIN Retweets r ON r.tid = f.tid AND r.usr IN Following
;
