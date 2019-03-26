<html>
<body>
<?php 
	

    if(isset($_POST["safe_url"])){
        if(isset($_POST["fileToDelete"])){

            $target_dir = "media/documents/" . $_POST["safe_url"] . "/";
            echo "$target_dir <br>";
            if(is_dir($target_dir)) {

                $target_file = $target_dir . basename($_POST["fileToDelete"]);
                echo "$target_file <br>";
                $deleteOk = 1;
                $imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));


                if(!file_exists($target_file)){
                    $deleteOK = 0;
                    echo "FilenoExist";
                }
                // Check if $deleteOk is set to 0 by an error
                if ($deleteOk == 0) {
                    echo "Sorry, your file was not deleted.";
                // if everything is ok, try to delete file
                }
                else
                {
                    chmod($target_file, 0777);
                    // chown($FileName,465);
                    if (unlink($target_file)){
                        echo "Successfully Deleted File" ;
                    }
                    else
                    {
                        echo "Sorry, there was an error deleting your file.";
                    }
                }
            }
        }
    }



?>


</body>
</html>