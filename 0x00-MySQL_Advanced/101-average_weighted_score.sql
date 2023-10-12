-- Creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  DECLARE user_id INT;
  DECLARE total_score FLOAT;
  DECLARE total_weight FLOAT;
  DECLARE ave_score FLOAT;
  DECLARE done INT DEFAULT 0;

  DECLARE cur CURSOR FOR SELECT id FROM users;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

  OPEN cur;
  
  user_loop: LOOP
    FETCH cur INTO user_id;
    
    IF done = 1 THEN
      LEAVE user_loop;
    END IF;
    
    SET total_score = 0;
    SET total_weight = 0;

    SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
    INTO total_score, total_weight
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;
    
    IF total_weight > 0 THEN
      SET ave_score = total_score / total_weight;
    ELSE
      SET ave_score = 0;
    END IF;
    
    UPDATE users
    SET average_score = ave_score
    WHERE id = user_id;
  END LOOP;
  
  CLOSE cur;
END //
DELIMITER ;
