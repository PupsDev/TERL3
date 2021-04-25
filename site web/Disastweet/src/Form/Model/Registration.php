<?php
namespace App\Form\Model;

use App\Document\UserSymfony;
use Symfony\Component\Validator\Constraints as Assert;

class Registration {
     /**
     * @Assert\Type(type="App\Document\UserSymfony")
     */
    protected $user;
    
    /**
     * @Assert\NotBlank()
     * @Assert\IsTrue()
     */
    protected $termsAccepted;
    
    public function setUser(UserSymfony $user)
    {
        $this->user = $user;
    }

    public function getUser()
    {
        return $this->user;
    }

    public function getTermsAccepted()
    {
        return $this->termsAccepted;
    }

    public function setTermsAccepted($termsAccepted)
    {
        $this->termsAccepted = (bool) $termsAccepted;
    }
}
