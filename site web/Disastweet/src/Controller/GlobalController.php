<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class GlobalController extends AbstractController {

    /**
     * @Route("/", name="app_home")
     */
    public function index(): Response {
        return $this->render('global/index.html.twig', [
                    'controller_name' => 'GlobalController',
        ]);
    }

    /**
     * @Route("/testpy")
     */
    public function testPy(): Response {
        $bearer = "AAAAAAAAAAAAAAAAAAAAADAyLgEAAAAAc4eGilNnzVuxnuvfEZjxh%2BU7P74%3D4GbSIUdOdwOLnZ8ClQU8dtEGy6nz8ijBZs0sxZioTCskVyxNjY";

        $db = $this->getParameter("mongodb.sslacces");
        $maxpage = 3;
        $keyword = "Saturne";
        //$command = "/usr/bin/python3 /home/terl3/www/site/disastweet/python/backend.py \"$db\" \"$bearer\" $maxpage \"$keyword\"";
        //$command = "pip install pymongo";
        //$command = 'pip freeze';
        //$output = shell_exec($command);
        $output = shell_exec($command . ' 2>&1'); //Pour le DEBUG
        dump($output);
        return $this->render('base.html.twig');
    }

    /**
     * @Route("/test");
     */
    public function test(): Response {
        $url = "http://127.0.0.1:8080/";
        $donnees = ['db_url' => $this->getParameter("mongodb.sslaccess"),
            "bearer_token" => "AAAAAAAAAAAAAAAAAAAAADAyLgEAAAAAc4eGilNnzVuxnuvfEZjxh%2BU7P74%3D4GbSIUdOdwOLnZ8ClQU8dtEGy6nz8ijBZs0sxZioTCskVyxNjY",
            "max_pages" => 1,
            "keyword" => "tornado",
        ];
        //$value = file_get_contents("http://127.0.0.1:8080/?db_url=$db_url&bearer_token=$bearer&max_pages=$max_pages&keyword=$keyword"); // Get send
        //Post send
        $options = array(
            'http' => array(
                'header' => "Content-type: application/x-www-form-urlencoded\r\n",
                'method' => 'POST',
                'content' => json_encode($donnees),
                'timeout' => -1.0,
            )
        );
        $context  = stream_context_create($options);
        $result = file_get_contents($url, false, $context);
        dump($result);
        return $this->render('base.html.twig');
    }

}
