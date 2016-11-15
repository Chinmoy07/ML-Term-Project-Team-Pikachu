<?php
	
	$begin_date = "2014-10-30";
	$end_date = "2016-10-31";
	set_time_limit(-1);
	

	$obj_arr =  json_decode( file_get_contents("../Outputs/tweets.json", "r") )->{"tweets"} ;
	$page = 1;
	$last_page = 1000;
	while( $page <= $last_page )
	{
		echo $page."<br>";
			$curl = curl_init();
			curl_setopt($curl, CURLOPT_PROXYTYPE, "HTTP");
			curl_setopt($curl, CURLOPT_PROXY, "10.3.100.207");
			curl_setopt($curl, CURLOPT_PROXYPORT, "8080");
			curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
			curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
			curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
			$query = array(
			  "api-key" => "8aae31b3-649c-428b-97f1-ea166ff79649",
			  "q" => "stock market",
			  "order-by" => "newest",
			  "from-date" =>  $begin_date ,
			  "to-date" => $end_date,
			  "page" => strval( $page )
			);
			
			$url = "http://content.guardianapis.com/search" . "?" . http_build_query($query);
			curl_setopt($curl, CURLOPT_URL, $url );
			
			try
			{
				$result = json_decode(curl_exec($curl));
				$last_page = $result->{"response"}->{"pages"};
				$length = sizeof( $result->{"response"}->{"results"} );
				
				$news = $result->{"response"}->{"results"};
				for( $i = 0; $i < sizeof($news); $i++ ) {
				$obj = json_decode('{}');
					$obj->{"text"} = $news[$i]->{"webTitle"};
					$obj->{"date"} =  str_replace( "Z", "", str_replace("T", " ", $news[$i]->{"webPublicationDate"}) );
					array_push($obj_arr, $obj);
				}
			}
			catch(Exception $e)
			{
				echo "error";
			}

			$page += 1;	
	}
	
	$tweets_obj = json_decode('{}');
	$tweets_obj->{"tweets"} = $obj_arr;
	$tweets_file = fopen("../Outputs/tweets.json", "w");

	fwrite( $tweets_file , json_encode($tweets_obj));

?>