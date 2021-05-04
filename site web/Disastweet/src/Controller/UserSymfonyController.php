<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Security\Core\Security;
use Symfony\Component\HttpFoundation\Request;
use Doctrine\ODM\MongoDB\DocumentManager;
use App\Repository\UserSymfonyRepository;
use App\Repository\TweetRepository;

class UserSymfonyController extends AbstractController {

    /**
     * @Route("/me/old", name="user_me_old")
     */
    public function me(Security $security): Response {
        $this->denyAccessUnlessGranted('ROLE_USER');

        return $this->render('user_symfony/me.html.twig', [
        ]);
    }

    /**
     * @Route("/me", name="user_me")
     */
    public function meAllInOne(Security $security, UserSymfonyRepository $userRepository, TweetRepository $tweetRepository): Response {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $keywords = [];
        
        //Read keywords 
        $fichier = fopen($this->getParameter("location.python") . "keyWord.txt", "r") or null;
        if($fichier != null){
            while(!feof($fichier)){
                array_push($keywords, strtolower(trim(fgets($fichier))));
            }
            fclose($fichier);
        }
        if ($this->isGranted('ROLE_ADMIN')) {
            $users = $userRepository->getAll();
            $reported = $tweetRepository->getAllValidReported();
            return $this->render('user_symfony/me_aio.html.twig', [
                        'users' => $users,
                        'reported' => $reported,
                        'autoload' => false,
                        'aio' => true,
                        'keywords' => $keywords,
            ]);
        }
        return $this->render('user_symfony/me_aio.html.twig', [
                    'autoload' => false,
                    'aio' => true,
                    'keywords' => $keywords,
        ]);
    }

    /**
     * @Route("/me/map", name="user_map")
     */
    public function map(Security $security): Response {
        $this->denyAccessUnlessGranted('ROLE_USER');

        return $this->render('user_symfony/map.html.twig', [
        ]);
    }

    /**
     * @Route("/me/addKey", name="user_add_key", methods={"POST"})
     */
    public function addKey(DocumentManager $dm, Security $security, Request $request) {
        if ($security->getUser() == null) {
            return $this->json(['reussite' => false, 'error' => 'not_connected']);
        }

        $keyword = trim($request->request->get('keyword'));
        if (strlen($keyword) <= 0) {
            return $this->json(['reussite' => false, 'error' => 'no_keyword']);
        }

        if (preg_match('/[^a-zA-Z0-9]+/', $keyword)) {
            return $this->json(['reussite' => false, 'error' => 'invalid_keyword']);
        }

        if (!$security->getUser()->addKeyword($keyword)) {
            return $this->json(['reussite' => false, 'error' => 'already_set_keyword']);
        }

        try {
            $dm->flush();
        } catch (\Doctrine\ODM\MongoDB\MongoDBException $ex) {
            return $this->json(['reussite' => false, 'error' => $ex->getMessage()]);
        }

        return $this->json(['reussite' => true, 'keyword' => $keyword]);
    }

    /**
     * @Route("/me/removeKey", name="user_remove_key", methods={"POST"})
     */
    public function removeKey(DocumentManager $dm, Security $security, Request $request) {
        if ($security->getUser() == null) {
            return $this->json(['reussite' => false, 'error' => 'not connected']);
        }

        $keyword = trim($request->request->get('keyword'));
        if (strlen($keyword) <= 0) {
            return $this->json(['reussite' => false, 'error' => 'no keyword']);
        }
        $security->getUser()->removeKeyword($keyword);
        try {
            $dm->flush();
        } catch (\Doctrine\ODM\MongoDB\MongoDBException $ex) {
            return $this->json(['reussite' => false, 'error' => $ex->getMessage()]);
        }

        return $this->json(['reussite' => true, 'keyword' => $keyword]);
    }

    /**
     * @Route("/me/extract_tweets", name="user_extract_tweets", methods={"POST"})
     */
    public function extractTweet(Security $security, Request $request) {
        if ($security->getUser() == null) {
            return $this->json(['reussite' => false, 'error' => 'not connected']);
        }
        $tweeterKey = $security->getUser()->getClefTwitter();
        $keywords = $security->getUser()->getKeywords();
        if ($tweeterKey == null || $tweeterKey == "") {
            return $this->json(['reussite' => false, 'error' => 'no tweeter key']);
        }
        if (sizeof($keywords) <= 0) {
            return $this->json(['reussite' => false, 'error' => 'no keyword']);
        }
        $db = $this->getParameter("mongodb.sslaccess");
        $exe = $this->getParameter("location.python");
        //$command = "python3 " . $exe . "backend.py '$db' '$tweeterKey' '1' '" . escapeshellcmd(implode("", $keywords)) . "'";
        $command = "python3 " . $exe . "backend.py '$db' '$tweeterKey' '1' '" . $keywords[0] . "'";
        //$output = shell_exec($command);
        $output = shell_exec($command . ' 2>&1'); //Pour le DEBUG
        //$process = new \Symfony\Component\Process\Process(['python3', $exe . "backend.py", $db ,$tweeterKey, 1, $keywords[0]]);

        return $this->json(['reussite' => true, 'command' => $command, 'output' => $output]);
    }

    /**
     * @Route("/me/update_twitter_key", name="user_update_twitter_key", methods={"POST"})
     */
    public function updateTwitterKey(DocumentManager $dm, Security $security, Request $request) {
        if ($security->getUser() == null) {
            return $this->json(['reussite' => false, 'error' => 'not connected']);
        }
        if (trim($request->request->get('key')) == "") {
            return $this->json(['reussite' => false, 'error' => 'no key']);
        }
        $security->getUser()->setClefTwitter(trim($request->request->get('key')));
        $dm->flush();
        return $this->json(['reussite' => true]);
    }

    /**
     * @Route("/me/map/reportTweet", name="map_report_tweet", methods={"POST"})
     */
    public function reportTweet(TweetRepository $repository, Security $security, Request $request) {
        if ($security->getUser() == null) {
            return $this->json(['reussite' => false, 'error' => 'not connected']);
        }
        $id = $request->request->get('id');
        $tweet = $repository->getOneByID($id);
        $invalide = false;
        if ($this->isGranted('ROLE_ADMIN')) {
            $invalide = $request->request->get('invalide');
        }
        if ($invalide) {
            $tweet->setValid('false');
        } else {
            if (!$tweet->isReportedBy($security->getUser()->getUsername())) {
                $tweet->addReport($security->getUser()->getUsername());
            } else {
                return $this->json(['reussite' => false, 'error' => 'already report']);
            }
        }

        $repository->flush();
        return $this->json(['reussite' => true]);
    }

}
