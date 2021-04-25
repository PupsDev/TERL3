<?php

namespace App\Repository;

use Doctrine\ODM\MongoDB\DocumentManager;
use App\Document\UserSymfony;

class UserSymfonyRepository {

    private $repos;
    private $dm;

    public function __construct(DocumentManager $dm) {
        $this->dm = $dm;
        $this->repos = $dm->getRepository(UserSymfony::class);
    }

    public function getAll(){
        return $this->repos->findAll();
    }

    public function flush() {
        $this->dm->flush();
    }

}
