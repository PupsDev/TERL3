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
        $command = "/usr/bin/python3 /home/terl3/www/site/disastweet/python/backend.py \"$db\" \"$bearer\" $maxpage \"$keyword\"";
        dump($command);
        //$output = shell_exec($command);
        $output = shell_exec($command.' 2>&1');//Pour le DEBUG
        dump($output);
        return $this->render('base.html.twig');
    }

}
