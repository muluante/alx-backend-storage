-- Creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
  DECLARE total_score FLOAT;
  DECLARE total_weight FLOAT;
  DECLARE ave_score FLOAT;

  SELECT SUM(corrections.score * projects.weight) INTO total_score
  FROM corrections
  JOIN projects ON corrections.project_id = projects.id
  WHERE corrections.user_id = user_id;

  SELECT SUM(projects.weight) INTO total_weight
  FROM corrections
  JOIN projects ON corrections.project_id = projects.id
  WHERE corrections.user_id = user_id;

  SET ave_score = total_score / total_weight;

  UPDATE users
  SET average_score = ave_score
  WHERE id = user_id;
END //
DELIMITER ;
