# niiif-niiif-annotations
# Script de génération d'un manifest IIIF pour le déposer dans Nakala

Fork du script [niiif-niiif](https://gitlab.huma-num.fr/jpressac/niiif-niiif)
créé par jpressac pour la création de manifestes IIIF et versement dans l'entrepôt de données Huma-Num Nakala.

Ce script a été développé dans le cadre du projet [Index CollexAngkor](https://www.collexpersee.eu/projet/indexangkor/) entre septembre 2022 et Juillet 2024 et financé par [Collex Persée](https://www.collexpersee.eu/).

## Objectifs du script niiif-niiif initial

- [ ] Vérifier si la donnée Nakala dont l'identifiant lui est donné en paramètre
existe.
- [ ] Le cas échéant, supprimer s'il existe l'ancien fichier metadata.json des
fichiers de la donnée.
- [ ] Créer un manifeste IIIF à partir des fichiers JPEG ou TIFF de la donnée
Nakala.
- [ ] Ajouter une annotation, provenant de la préparation Tropy, à chaque fichier
image de la donnée Nakala.
- [ ] Ajouter à la donnée Nakala le fichier metadata.json contenant le manifeste
et le fichier d'annotations Tropy.
- [ ] Générer un fichier CSV en sortie.

## Ajouts par rapport au script original

- Ajout des annotations au manifest à partir d'un fichier d'annotations JSON-LD extrait depuis le logiciel
Tropy
- Construction de la "target" : coordonnées de la boîte de sélection liée à l'annotation
- Construction d'un système de comptage des annotations dans le cas d'une page
avec plusieurs annotations
- Récupération des métadonnées depuis Nakala
- Gestion des PDF dans le manifeste pour le rendre disponible au téléchargement
dans un visualiseur
- Création des classes:  Connection_Nakala, Metadata, Annotation et Manifest
- Upload du fichier JSON des annotations Tropy dans Nakala
- Ajout de la déclaration d'un service API search v1 au manifest généré


## Utilisation

### Prérequis

- Python >= 3.7
- Installation des dépendances nécessaires au script :

```bash
pip install -r requirements.txt
```

- Le fichier JSON d'annotations extrait depuis Tropy
- Le fichier CSV contenant les identifiants des données Nakala à traiter

### Utilisation du script

La commande suivante lance le script avec tous les paramètres. Dans un vrai usage ils ne seront pas tous utilisés:

```bash
python manifest_iiif -dataid {identifiant de la donnée Nakala} -apikey {clé d\'API}   -annotfile {fichier JSON d\'annotations} -typeannot {type d\'annotation} -isprod {True ou False} -csvfile {fichier CSV} -csvoutput {fichier CSV de sortie} -baseUrl {Base Url} -method {méthode de génération des annotations IIIF} -searchUrl {Base d'URL servant pour un service search IIIF}
```

### Paramètres obligatoires

- **-apikey** : clé d'API du compte utilisateur Nakala
- **-dataid**: id de la ressource nakala

Si vous utilisez un fichier CSV il faut (cf. fichier id_nakala_example.csv):
- utiliser le caractère ";" comme séparateur de colonne
- nommer les deux colonnes obligatoires respectivement "dcterms:identifier" et "annotation_file", même si la colonne annotation_file est vide (dans une configuration où on verse les manfestes en lot mais sans annotations).

### Paramètres optionnels

- **-typeannot** : type d'annotation (par défaut : "plain"). Les valeurs possibles
sont "*plain*" ou "*html*". "*html*" sera utilisé lorsqu'on souhaite ajouter de la mise en forme au contenu. Par eemple, les balises comme "<p></p>" seront interprétées. En "*plain*" elles ne le seront pas.
- **-isprod**: True ou False. True si l'on souhaite interroger l'API Nakala ou False
si l'on souhaite interroger l'API de test Nakala (si paramètre non saisi, la valeur par défaut est "False" et donc test.nakala.fr)
- **-annotfile** : fichier JSON d'annotations extrait depuis Tropy
(par défaut : "annotations.json")
- **-csvfile** : fichier CSV contenant les identifiants des données Nakala à traiter.
Ce paramètre prend en charge les paramètres *dataid* et *annotfile* sous la forme des colonnes "dcterms:identifier;annotation_file" séparées par un ";" et encodé en utf-8.

- **-csvoutput** : chemin du fichier CSV de sortie contenant l'URL du manifest généré et son identifiant Nakala associé
- **-searchUrl** pour déclaration d'un service search API v1 dans le manifest et définition de son URL de base et de son préfix: Par exemple pour la bibliothèque EFEO c'est : https://banyan.efeo.fr/iiif-annot-search
- **-method** est utilisé uniquement pour la génération des annotations et n'est pas nécessaire pour un manifets simple sans annotations. Il prend 2 valeurs possibles :
  - "*name*", valeur par défaut si aucun paramètre n'est saisi. Les annotations sont générées en vérifiant bien que les noms des fichiers annotées correspondent bien à ceux dans Nakala (très long)
  - "*sha1*", même chose que name mais vérifie le sha1 à la place du nom de fichier (peut être très long si beaucoup de fichiers)

### Exemples
**Génération et versement d'un manifest simple sur la platefome de test.nakala.fr**: 

```bash
python manifest_iiif -dataid 10.34847/nkl.3c8b7258 -apikey 01234567-89ab-cdef-0123-456789abcdef

```

**Génération et versement de manifest en lot (via csv) sur la platefome de test.nakala.fr**:

```bash
python manifest_iiif -csvfile ./id_nakala_example.csv"  -isprod False -apikey 01234567-89ab-cdef-0123-456789abcdef
```
**Génération et versement d'un manifest avec annotations sur la platefome de test.nakala.fr** (avec en paramètre un fichier d'annotations json exporté depuis Tropy): 

```bash
python manifest_iiif -dataid 10.34847/nkl.3c8b7258 -isprod False -apikey 01234567-89ab-cdef-0123-456789abcdef -annotfile ./tropy.json
```


**Génération et versement d'un manifest avec annotations et décalartion du service search sur la platefome de test.nakala.fr**: 

```bash
python manifest_iiif -dataid 10.34847/nkl.3c8b7258 -isprod True -apikey 01234567-89ab-cdef-0123-456789abcdef -annotfile ./tropy.json -searchUrl https://banyan.efeo.fr/iiif-annot-search
```

### Description des classes

- La classe **Manifest** permet de créer un manifeste IIIF à partir des fichiers
JPEG ou TIFF d'une donnée Nakala. Elle permet également d'ajouter ou non
une annotation à chaque fichier image de la donnée Nakala.
- La classe **Annotation** permet de créer une annotation à partir d'un fichier
JSON extrait depuis le logiciel Tropy. Elle permet également de créer la "target" :
endroit auquel l'annotation est rattachée.
- La classe **Metadata** permet de récupérer les métadonnées d'une donnée Nakala.
- La classe **Connection_Nakala** permet de vérifier si la donnée Nakala dont
l'identifiant lui est donné en paramètre existe. Elle permet également de supprimer
l'ancien fichier metadata.json des fichiers de la donnée et d'ajouter à la donnée
Nakala le fichier metadata.json contenant le manifeste.
- La classe **Parsing_csv** permet de récupérer les différentes ressources Nakala
à traiter pour créer leur manifeste respectif.
- La classe **Config** permet de récupérer les différents paramètres nécessaires
à la création des manifestes (API headers, arguments des URL).
- La classe **Output** permet de générer un fichier CSV en sortie contenant
l'URL du manifest généré et son identifiant Nakala associé.
- La classe **Reorder** permet de placer le fichier manifest metadata.json comme premier 
de la liste des fichiers d'une ressource nakala (nécessaire pour le fonctionnement de l'uri en https://nakala.fr/data/{identifiant}).


## TODO

1) modifier annotation.py. la propriété body renvoie actuellement une liste alors qu'elle ne devrait renvoyer qu'un dictionnaire entre {}. Faire également la modification dans le module iiif annot search lorsqu'on parse le body. Actuellement body[0]['value'] et ça deviendra body['value'] (a vérifier)
            

### Membres du projet

Vincent Paillusson,
Léandro Encarnaçao

