<?php

namespace App\Document;

use Symfony\Component\Security\Core\User\UserInterface;
use Doctrine\Bundle\MongoDBBundle\Validator\Constraints\Unique as MongoDBUnique;
use Doctrine\ODM\MongoDB\Mapping\Annotations as MongoDB;
use Symfony\Component\Validator\Constraints as Assert;

/**
 * @MongoDB\Document(db="disastweet", collection="user_symfony")
 * @MongoDBUnique(fields="email")
 */
class UserSymfony implements UserInterface {

    /**
     * @MongoDB\Id(type="string", name="email",strategy="NONE")
     * @Assert\NotBlank()
     * @Assert\Email()
     */
    private $email;

    /**
     * @MongoDB\Field(type="string", name="alias", nullable=true)
     */
    private $alias;

    /**
     * @MongoDB\Field(type="string", name="password", nullable=false)
     * @Assert\NotBlank()
     */
    private $password;

    /**
     * @MongoDB\Field(type="string", name="clef-twitter", nullable=true)
     */
    private $clefTwitter;

    /**
     * @MongoDB\Field(type="collection", name="keywords", nullable=true)
     */
    private $keywords = [];

    /**
     * @MongoDB\Field(type="collection", name="roles", nullable=true)
     */
    protected $roles = [];

    function getEmail() {
        return $this->email;
    }

    function getNom() {
        return $this->nom;
    }

    function getPrenom() {
        return $this->prenom;
    }

    function getAlias() {
        return $this->alias;
    }

    function getPassword() {
        return $this->password;
    }

    function getClefTwitter() {
        return $this->clefTwitter;
    }

    function getKeywords(): array {
        if ($this->keywords == null) {
            return [];
        }
        return array_unique($this->keywords);
    }

    function getRoles(): array {
        $roles = $this->roles;
        // guarantee every user at least has ROLE_USER
        $roles[] = 'ROLE_USER';
  /*      if ($this->isRole('ROLE_SUPERADMIN') && !$this->isRole('ROLE_ADMIN')) {
            $roles[] = 'ROLE_ADMIN';
        }
        if (($this->isRole('ROLE_SUPERADMIN') || $this->isRole('ROLE_ADMIN')) && !$this->isRole('ROLE_VALIDATOR')) {
            $roles[] = 'ROLE_VALIDATOR';
        }*/
        return array_unique($roles);
    }

    function setEmail($email): self {
        $this->email = $email;
        return $this;
    }

    function setNom($nom): self {
        $this->nom = $nom;
        return $this;
    }

    function setPrenom($prenom): self {
        $this->prenom = $prenom;
        return $this;
    }

    function setAlias($alias): self {
        $this->alias = $alias;
        return $this;
    }

    function setPassword($password): self {
        $this->password = $password;
        return $this;
    }

    function setClefTwitter($clefTwitter): self {
        $this->clefTwitter = $clefTwitter;
        return $this;
    }

    function setKeywords($keywords): self {
        $this->keywords = $keywords;
        return $this;
    }

    function addKeyword($keyword): bool {
        if (!isset($this->keywords)) {
            $this->keywords = [];
        }
        if (array_search($keyword, $this->keywords) === false) {
            $this->keywords[] = $keyword;
            return true;
        }
        return false;
    }

    function removeKeyword($keyword): self {
        if (($key = array_search($keyword, $this->keywords)) !== false) {
            unset($this->keywords[$key]);
        }
        return $this;
    }

    function setRoles($roles): self {
        $this->roles = $roles;
        return $this;
    }

    public function isRole($role): bool {
        if (array_search($role, $this->getRoles()) == false) {
            return false;
        }
        return true;
    }

    public function removeRole($role): self {
        $val = array_search($role, $this->roles);
        if ($val != false) {
            unset($this->roles[$val]);
        }
        return $this;
    }

    public function addRole($role): self {
        if (!$this->isRole($role)) {
            $this->roles[] = $role;
        }
        return $this;
    }

    public function eraseCredentials() {
        
    }

    public function getSalt() {
        
    }

    public function getUsername(): string {
        return $this->email;
    }

}
