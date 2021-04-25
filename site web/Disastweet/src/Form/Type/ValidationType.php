<?php

namespace App\Form\Type;

use App\Document\TweetDocument;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Component\Form\Extension\Core\Type\HiddenType;

/**
 * Description of ValidationType
 *
 * @author florentin.denis@etu.umontpellier.fr
 */
class ValidationType extends AbstractType {

    public function buildForm(FormBuilderInterface $builder, array $options) {
        //HiddenFile for selection
        //Candidats
        $builder->add('selection_candidats', HiddenType::class, [
            'required' => false,
            'mapped' => false,
        ]);
        //Evenements
        $builder->add('selection_events', HiddenType::class, [
            'required' => false,
            'mapped' => false,
        ]);
        //SUBMIT
        $builder->add('valid', SubmitType::class, [
                    'label' => 'Valide',
                    'attr' => ['class' => 'btn btn-success form-control mt-1'],
                ])
                ->add('invalid', SubmitType::class, [
                    'label' => 'Invalide',
                    'attr' => ['class' => 'btn btn-danger form-control mt-1'],
                ])
                ->add('hs', SubmitType::class, [
                    'label' => 'Hors Sujet',
                    'attr' => ['class' => 'btn btn-warning form-control mt-1'],
                ])
        ;
    }

    public function configureOptions(OptionsResolver $resolver) {
        $resolver->setDefaults([
            'data_class' => TweetDocument::class,
        ]);
    }

}
