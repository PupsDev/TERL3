<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Request;
use App\Repository\TweetRepository;
use App\Form\Type\ValidationType;
use Doctrine\ODM\MongoDB\DocumentManager;
use App\Document\TweetDocument;

class ValidationController extends AbstractController {

    /**
     * @Route("/validation", name="validation")
     */
    public function validation(DocumentManager $dm, TweetRepository $repository, Request $request): Response {
        $this->denyAccessUnlessGranted('ROLE_VALIDATOR');
        $tweet = $repository->getOneToValidate();
        if ($tweet != null) {
            $form = $this->createForm(ValidationType::class, $tweet, []);
            $form->handleRequest($request);
            $error_no_selection = false;
            if ($form->isSubmitted() && $form->isValid()) {
                if ($this->updateTweet($dm, $repository, $form, $tweet)) {
                    return $this->redirectToRoute("validation");
                }
                $error_no_selection = true;
            }
            return $this->render('validation/validation.html.twig', [
                        'tweet' => $tweet,
                        'candidates' => $tweet->getSpacy()['candidates'],
                        'events' => $tweet->getSpacy()['events'],
                        'form' => $form->createView(),
                        'error_no_selection' => $error_no_selection,
            ]);
        }
        return $this->render('validation/validation.html.twig', [
                    'tweet' => $tweet,
        ]);
    }

    private function updateTweet(DocumentManager $dm, TweetRepository $repository, $form, TweetDocument $tweet) {
        if ($form->get('valid')->isClicked()) {
            $tweet->setValid("true");
            $candidats = strlen(trim($form->get('selection_candidats')->getData())) > 0 ? explode(',', trim($form->get('selection_candidats')->getData())) : [];
            $events = strlen(trim($form->get('selection_events')->getData())) > 0 ? explode(',', trim($form->get('selection_events')->getData())) : [];

            if (sizeof($candidats) == 0 || sizeof($events) == 0) {
                return false;
            }
            foreach ($candidats as $candidat) {
                $geo = json_decode(file_get_contents("http://api.geonames.org/searchJSON?q=$candidat&maxRows=1&username=doublepups"), true);
                if ($geo['totalResultsCount'] > 0) {
                    $tweet->addValidationPlace($candidat, $geo['geonames'][0]['lng'], $geo['geonames'][0]['lat']);
                } else {
                    $tweet->addValidationPlaceNoCoord($candidat);
                }
            }
            foreach ($events as $evenement) {
                $tweet->addValidationEvent($evenement);
            }
        } else if ($form->get('invalid')->isClicked()) {
            $tweet->setValid("false");
        } else if ($form->get('hs')->isClicked()) {
            $dm->remove($tweet);
        }
        $repository->flush();
        return true;
    }

    /**
     * @Route("/validation/get", name="validation_get_tweet", methods={"POST"})
     */
    public function getTweet(TweetRepository $repository, Request $request) {
        if (!$this->isGranted('ROLE_VALIDATOR')) {
            return $this->json(['reussite' => false, 'error' => 'not_validator']);
        }
        $tweet = $repository->getOneToValidate();
        return $this->json(['reussite' => true, 'tweet' => $tweet]);
    }

    /**
     * @Route("/validation/validate", name="validation_validate_tweet", methods={"POST"})
     */
    public function validateTweet(DocumentManager $dm, TweetRepository $repository, Request $request) {
        if (!$this->isGranted('ROLE_VALIDATOR')) {
            return $this->json(['reussite' => false, 'error' => 'not_validator']);
        }
        $status = $request->request->get('status');
        $tweet = $repository->getOneByID($request->request->get('tweet')['id']);
        if ($status == "valid") {
            $lieux = $request->request->get('lieux');
            $events = $request->request->get('events');
            if( ($events == null && $events == null) || (sizeof($lieux) <= 0 && sizeof($events) <= 0)){
                return $this->json(['reussite' => false, 'error' => 'no_candidates_and_events']);
            }
            if ($events == null || sizeof($lieux) <= 0) {
                return $this->json(['reussite' => false, 'error' => 'no_candidates']);
            }
            if ( $events == null ||  sizeof($events) <= 0) {
                return $this->json(['reussite' => false, 'error' => 'no_events']);
            }
            $tweet->setValid("true");
            foreach ($lieux as $candidat) {
                $geo = json_decode(file_get_contents("http://api.geonames.org/searchJSON?q=$candidat&maxRows=1&username=doublepups"), true);
                if ($geo['totalResultsCount'] > 0) {
                    $tweet->addValidationPlace($candidat, $geo['geonames'][0]['lng'], $geo['geonames'][0]['lat']);
                } else {
                    $tweet->addValidationPlaceNoCoord($candidat);
                }
            }
            foreach ($events as $evenement) {
                $tweet->addValidationEvent($evenement);
            }
        } else if ($status == "invalid") {
            $tweet->setValid("false");
        } else if ($status == "hs") {
            $dm->remove($tweet);
        }
        $dm->flush();
        return $this->json(['reussite' => true]);
    }

}
