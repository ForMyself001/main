INSERT INTO messages (user, message)
SELECT DISTINCT u.user, 'есть запись'
FROM (
    SELECT DISTINCT user
    FROM users
    WHERE substr(datastr, 1, 2) || '-' || substr(datastr, 3, 2) || '-' || substr(datastr, 5, 2) >= date('now', '-7 days')
) AS u
WHERE (
    SELECT COUNT(*)
    FROM (
        SELECT DISTINCT substr(datastr, 1, 2) || '-' || substr(datastr, 3, 2) || '-' || substr(datastr, 5, 2) AS day
        FROM users
        WHERE user = u.user
        AND substr(datastr, 1, 2) || '-' || substr(datastr, 3, 2) || '-' || substr(datastr, 5, 2) >= date('now', '-7 days')
        GROUP BY day
    )
) = 7;