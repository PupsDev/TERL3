<?php

namespace App\Form\Type;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\CheckboxType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class RegistrationType extends AbstractType {

    public function buildForm(FormBuilderInterface $builder, array $options) {
        $builder->add('user', UserSymfonyType::class);
        $builder->add('terms', CheckboxType::class, [
            'property_path' => 'termsAccepted',
            'label' => 'form.terms'
        ]);
    }

    public function configureOptions(OptionsResolver $resolver) {
        
        $resolver->setDefaults([
            'translation_domain' => 'form',
        ]);
    }

}
