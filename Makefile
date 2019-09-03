competition/scoring.zip: scoring/*
	cd scoring && zip ../competition/scoring.zip * && cd ..

competition/starting_kit.zip: starting_kit/*
	cd starting_kit && zip ../competition/starting_kit.zip * && cd ..

competition/trial_data.zip: trial_data/*
	cd trial_data && zip ../competition/trial_data.zip * && cd ..

competition/trial_reference.zip: trial_reference/*
	cd trial_reference && zip ../competition/trial_reference.zip * && cd ..

competition/test_reference.zip: test_reference/*
	cd test_reference && zip ../competition/test_reference.zip * && cd ..

competition.zip: competition/* competition/scoring.zip competition/starting_kit.zip competition/trial_data.zip competition/trial_reference.zip competition/test_reference.zip
	cd competition && zip ../competition.zip * && cd ..
