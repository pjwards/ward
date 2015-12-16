SELECT
	UG.fbuser_id as user_id,
	UG.group_id as group_id,
	(SELECT count(*) FROM archive_post WHERE group_id = '373189689430865' AND user_id = UG.fbuser_id) as post_count,
	(SELECT count(*) FROM archive_comment WHERE group_id = '373189689430865' AND user_id = UG.fbuser_id) as comment_count
FROM
	archive_fbuser_groups as UG
INNER JOIN archive_fbuser as U
ON UG.fbuser_id = U.id
WHERE UG.group_id = '373189689430865'
ORDER BY U.name;

SELECT
	id
FROM
	archive_group;

INSERT INTO archive_useractivity(user_id, group_id, post_count, comment_count)
SELECT
	UG.fbuser_id as user_id,
	UG.group_id as group_id,
	(SELECT count(*) FROM archive_post WHERE group_id = UG.group_id AND user_id = UG.fbuser_id) as post_count,
	(SELECT count(*) FROM archive_comment WHERE group_id = UG.group_id AND user_id = UG.fbuser_id) as comment_count
FROM
	archive_fbuser_groups as UG
INNER JOIN archive_fbuser as U
ON UG.fbuser_id = U.id;