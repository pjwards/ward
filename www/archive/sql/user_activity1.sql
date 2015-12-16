SELECT 
  user_id,
  count(user_id) as count
FROM 
  public.archive_post
WHERE
  group_id = '174499879257223'
GROUP BY user_id
ORDER BY count desc
LIMIT 10;

SELECT 
  user_id,
  count(user_id) as count
FROM 
  public.archive_comment
WHERE
  group_id = '183432721693235'
GROUP BY user_id
ORDER BY count desc
LIMIT 10;

SELECT 
  U.fbuser_id
FROM 
  public.archive_fbuser_groups as U,
  public.archive_post as P,
  public.archive_comment as C
WHERE
  U.group_id = '183432721693235'
GROUP BY U.fbuser_id
LIMIT 10;

SELECT
  U.fbuser_id,
  count(U.fbuser_id)
FROM
  public.archive_fbuser_groups as U
WHERE
  U.group_id = '183432721693235'
GROUP BY U.fbuser_id;

SELECT
  UG.fbuser_id as id,
  U.name as name,
  U.picture as picture,
  (SELECT count(*) FROM public.archive_post WHERE group_id = '183432721693235' AND user_id = UG.fbuser_id) as p_count,
  (SELECT count(*) FROM public.archive_comment WHERE group_id = '183432721693235' AND user_id = UG.fbuser_id) as c_count
FROM
  public.archive_fbuser_groups as UG
INNER JOIN public.archive_fbuser as U
ON UG.fbuser_id = U.id
WHERE
  UG.group_id = '183432721693235' AND U.name @@ '김슬'
ORDER BY U.name;

SELECT T.count, count(*) FROM
(SELECT 
  count(user_id) as count
FROM 
  public.archive_post
WHERE
  group_id = '183432721693235'
GROUP BY user_id) AS T
GROUP BY T.count
ORDER BY count(*) DESC
LIMIT 9;