<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Request;
use App\Repository\UserSymfonyRepository;
use Symfony\Component\Security\Core\Security;
use App\Repository\TweetRepository;

class AdministrationController extends AbstractController {

    /**
     * @Route("/administration", name="administration")
     */
    public function administration(UserSymfonyRepository $repository, Request $request): Response {
        $this->denyAccessUnlessGranted('ROLE_ADMIN');
        $users = $repository->getAll();
        return $this->render('administration/administration.html.twig', [
                    'users' => $users
        ]);
    }

    /**
     * @Route("/administration/save_role", name="admin_save_role", methods={"POST"})
     */
    public function sauvegardeRole(Security $security, UserSymfonyRepository $repository, Request $request): Response {
        $data = null;
        if ($security->getUser() == null) {
            return $this->json(['reussite' => false, 'error' => 'not_connected']);
        } else {
            $admin = $this->isGranted('ROLE_ADMIN');
            $superadmin = $security->isGranted('ROLE_SUPERADMIN');
            if (!$admin && !$superadmin) {
                return $this->json(['reussite' => false, 'error' => 'access_denied']);
            } else {
                $data = $request->get('data');
                $users = $repository->getAll();
                foreach ($data as $value) {
                    $email = $value["user"];
                    $validator = $value["validator"];
                    $admin = ($superadmin ? $value["admin"] : null);

                    $find = false;
                    for ($i = 0; $i < sizeof($users) && !$find; $i++) {
                        if (strcasecmp(trim($users[$i]->getEmail()), trim($email)) == 0) {
                            $find = true;
                            if ($validator == 'true') {
                                $users[$i]->addRole('ROLE_VALIDATOR');
                            } else if ($validator == 'false') {
                                $users[$i]->removeRole('ROLE_VALIDATOR');
                            }

                            if ($admin == 'true') {
                                $users[$i]->addRole('ROLE_ADMIN');
                            } else if ($admin == 'false') {
                                $users[$i]->removeRole('ROLE_ADMIN');
                            }
                            $repository->flush();
                        }
                    }
                }
            }
        }
        return $this->json(['reussite' => true]);
    }

    /**
     * @Route("/administration/tweet/invalide", name="admin_invalide_tweet", methods={"POST"})
     */
    public function tweetInvalide(Security $security, TweetRepository $repository, Request $request) {
        if ($security->getUser() == null) {
            return $this->json(['reussite' => false, 'error' => 'not_connected']);
        }
        if (!$this->isGranted('ROLE_ADMIN')) {
            return $this->json(['reussite' => false, 'error' => 'not_admin']);
        }
        $tweet = $repository->getOneByID($request->request->get('idTweet'));
        $tweet->setValid('false');
        $repository->flush();
        return $this->json(['reussite' => true]);
    }

    /**
     * @Route("/administration/tweet/reset_report", name="admin_reset_report_tweet", methods={"POST"})
     */
    public function tweetResetReport(Security $security, TweetRepository $repository, Request $request) {
        if ($security->getUser() == null) {
            return $this->json(['reussite' => false, 'error' => 'not_connected']);
        }
        if (!$this->isGranted('ROLE_ADMIN')) {
            return $this->json(['reussite' => false, 'error' => 'not_admin']);
        }
        $tweet = $repository->getOneByID($request->request->get('idTweet'));
        $tweet->resetReportedBy();
        $repository->flush();

        return $this->json(['reussite' => true]);
    }

}
