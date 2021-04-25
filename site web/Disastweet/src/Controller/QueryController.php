<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use App\Repository\TweetRepository;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Security\Core\Security;
use Symfony\Component\HttpFoundation\Request;

class QueryController extends AbstractController {

    /**
     * @Route("/me/map/keyword_query", name="map_keywordQuery", methods={"POST"})
     */
    public function keywordQuery(TweetRepository $repository, Request $request) {

        $keywords = $request->request->get('query'); //POST
        //$keywords = $request->query->get('query'); //GET
        $output = [];
        //Format a inserer dans output  ['keyword' => 'tornade', 'data' => [ /*tweets*/ ]]
        $datas = $repository->getAllByKeywords($keywords);
        foreach ($keywords as $value) {
            $output[] = ['keyword' => $value, 'data' => []];
        }

        while ($datas->valid()) { //vérifie si la donnée est valide
            $donnee = $datas->current(); //récupere la donnée actuelle
            $word = $donnee->getValidation()['events'];
            $max = sizeof($word);
            $count = 0;
            for ($i = 0; $i < sizeof($output) && $count < $max; $i += 1) {
                if (in_array($output[$i]['keyword'], $word)) {
                    array_push($output[$i]['data'], $donnee);
                    $count++;
                }
            }

            $datas->next(); //passe à la donnée suivante.
        }

        //return $this->render('base.html.twig'); //DEBUG
        return $this->json($output);
        //Format de sortie [['keyword' => 'un', 'data' => [ /*tweets*/ ]],['keyword' => 'deux', 'data' => [ /*tweets*/ ]],...]
    }

}
