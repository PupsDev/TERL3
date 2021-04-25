<?php

namespace App\Document;

use Doctrine\ODM\MongoDB\Mapping\Annotations as MongoDB;
use Symfony\Component\Validator\Constraints as Assert;
use Doctrine\Bundle\MongoDBBundle\Validator\Constraints\Unique as MongoDBUnique;
/**
 * @MongoDB\Document(db="disastweet", collection="spacetweets")
 * @MongoDBUnique(fields="id")
 */
class TweetDocument {

    /**
     * @MongoDB\Id(type="string", name="id", strategy="NONE")
     */
    private $id;

    /**
     * @MongoDB\Field(type="string", name="author_id")
     */
    private $author_id;

    /**
     * @MongoDB\Field(type="collection", name="place")
     */
    private $place;

    /**
     * @MongoDB\Field(type="string", name="geo")
     */
    private $geo;

    /**
     * @MongoDB\Field(type="string", name="valid")
     */
    private $valid;

    /**
     * @MongoDB\Field(type="string", name="place_user")
     */
    private $place_user;

    /**
     * @MongoDB\Field(type="string", name="real")
     */
    private $real;

    /**
     * @MongoDB\Field(type="string", name="text")
     */
    private $text;

    /**
     * @MongoDB\Field(type="collection", name="spacy")
     */
    private $spacy;

    /**
     * @MongoDB\Field(type="raw", name="validation")
     */
    private $validation;

    /**
     * @MongoDB\Field(type="collection", name="reported_by")
     */
    private $reportedBy = [];

    function getId() {
        return $this->id;
    }

    function getAuthor_id() {
        return $this->author_id;
    }

    function getAuthorId() {
        return $this->author_id;
    }

    function getPlace() {
        return $this->place;
    }

    function getGeo() {
        return $this->geo;
    }

    function getValid() {
        return $this->valid;
    }

    function getPlace_user() {
        return $this->place_user;
    }

    function getPlaceUser() {
        return $this->place_user;
    }

    function getReal() {
        return $this->real;
    }

    function getText() {
        return $this->text;
    }

    function getSpacy() {
        return $this->spacy;
    }

    function setPlace($place): void {
        $this->place = $place;
    }

    function setValid($valid): void {
        $this->valid = $valid;
    }

    function setSpacy($spacy): void {
        $this->spacy = $spacy;
    }

    function getValidation() {
        return $this->validation;
    }

    function setValidation($validation): void {
        $this->validation = $validation;
    }

    function addValidationPlaceNoCoord($place): void {
        $this->validation['places'][] = ['place' => $place, 'lng' => '0', 'lat' => '0'];
    }

    function addValidationPlace($place, $lng, $lat): void {
        $this->validation['places'][] = ['place' => $place, 'lng' => $lng, 'lat' => $lat];
    }

    function addValidationEvent($event): void {
        $this->validation['events'][] = $event;
    }

    function addReport($userId): void {
        $this->reportedBy[] = $userId;
    }

    function resetReportedBy(): void {
        $this->reportedBy = [];
    }

    function getReportedBy(): array {
        return $this->reportedBy;
    }

    function isReportedBy($userId): bool {
        $trouver = false;
        for ($i = 0; $i < sizeof($this->reportedBy) && !$trouver; $i++) {
            if (strcasecmp(trim($this->reportedBy[$i]), trim($userId)) == 0) {
                $trouver = true;
            }
        }
        return $trouver;
    }

}
