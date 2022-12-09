CREATE TABLE IF NOT EXISTS complaint (
	complaint_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
	last_name VARCHAR(50) NOT NULL,	
	first_name VARCHAR(50) NOT NULL,	
	patronymic VARCHAR(50),	
	phone VARCHAR(20) NOT NULL,	
	complaint_text TEXT NOT NULL,

	CONSTRAINT PK_complaint_complaint_id PRIMARY KEY(complaint_id)	
);

