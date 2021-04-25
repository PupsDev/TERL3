<?php

namespace App\Form\Type;

use App\Document\UserSymfony;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\EmailType;
use Symfony\Component\Form\Extension\Core\Type\PasswordType;
use Symfony\Component\Form\Extension\Core\Type\RepeatedType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class UserSymfonyType extends AbstractType {

    public function buildForm(FormBuilderInterface $builder, array $options) {
        $builder->add('email', EmailType::class, [
            'label' => 'form.email',
        ]);
        $builder->add('alias', TextType::class, [
            'required' => false,
            'label' => 'form.alias',
        ]);
        $builder->add('password', RepeatedType::class, [
            'first_options' => ['label' => 'form.password.primary',],
            'second_options' => ['label' => 'form.password.secondary',],
            'type' => PasswordType::class,
        ]);
        $builder->add('clefTwitter', TextType::class, [
            'required' => false,
            'label' => 'form.tweeter.key',
        ]);
    }

    public function configureOptions(OptionsResolver $resolver) {
        $resolver->setDefaults([
            'data_class' => UserSymfony::class,
            'translation_domain' => 'form',
        ]);
    }

}
