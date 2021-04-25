<?php

namespace App\Repository;

use Doctrine\ODM\MongoDB\DocumentManager;
use App\Document\TweetDocument;
use Doctrine\ODM\MongoDB\Iterator\CachingIterator;

/**
 * Description of TweetRepository
 *
 * @author florentin.denis@etu.umontpellier.fr
 */
class TweetRepository {

    private $repos;
    private $dm;

    public function __construct(DocumentManager $dm) {
        $this->dm = $dm;
        $this->repos = $dm->getRepository(TweetDocument::class);
    }

    public function getOneToValidate(): ?TweetDocument {
        return $this->repos->findOneBy(['valid' => '?']);
    }

    public function getOneByID($id): ?TweetDocument {
        return $this->repos->findOneBy(['id' => $id]);
    }

    public function flush() {
        $this->dm->flush();
    }

    public function getAllByKeywords($keywords): CachingIterator {
        return $this->dm->createQueryBuilder(TweetDocument::class)
                        ->find()
                        ->field('valid')->equals("true")
                        ->field('validation.events')->in($keywords)
                        ->getQuery()
                        ->execute();
    }

    public function getAllReportedByUser($idUser) {
        return $this->dm->createQueryBuilder(TweetDocument::class)
                        ->find()
                        ->field('reported_by')->in([$idUser])
                        ->getQuery()
                        ->execute();
    }

    public function getAllReported() {
        $qb = $this->dm->createQueryBuilder(TweetDocument::class);
        return $qb->find()
                        ->field('reported_by')->exists(true)->not($qb->expr()->size(0))
                        ->getQuery()
                        ->execute();
    }

}
