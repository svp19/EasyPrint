<html>
<body>
<?php 
	
	$target_dir = "media/documents/" . $_POST["safe_url"] . "/";
	echo "$target_dir";
	if(!is_dir($target_dir)) {
		mkdir($target_dir);
	}
	$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
	$uploadOk = 1;
	$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

	//Check extension
	if($imageFileType != "pdf"){

		echo " Error! Expected .pdf file only. All other types of files are not accepted.<br>";
		$uploadOk = 0 ;
	}

	// Check file size
	if ($_FILES["fileToUpload"]["size"] > 204800000) {
	    echo "Error, your file size is greater than 200mB! Please consult with admin.<br>";
	    $uploadOk = 0;
	}

	// Check if $uploadOk is set to 0 by an error
	if ($uploadOk == 0) {
	    echo "Sorry, your file was not uploaded.";
	// if everything is ok, try to upload file
	} 
	else 
	{
	    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
	        echo "Succesfully Uploaded File" ;
	    } 
	    else 
	    {
	        echo "Sorry, there was an error uploading your file.";
	    }
	}
?>
<br>


</body>
</html>