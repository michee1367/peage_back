


--- Quels sont les pourcentages des état d'avancement  de tous les projets programmés dans le grand kasai
SELECT pp.etat_projet, count(pp.id) nombre, CONCAT(ROUND((count(pp.id)*100.0)/ (SELECT COUNT(*) FROM public.projet_programme), 2),' %') AS pourcentage
	FROM public.projet_programme pp
	INNER JOIN public.territoire_ville t on t.id = pp.territory_id
	INNER JOIN public.provinces p on p.id = t.province_id
	where p.id > 21
	group by pp.etat_projet
;
--- Quels sont les pourcentages des type projet  de tous les projets programmés
SELECT pp.type, count(pp.id) nombre, CONCAT(ROUND((count(pp.id)*100.0)/ (SELECT COUNT(*) FROM public.projet_programme), 2),' %') AS pourcentage
	FROM public.projet_programme pp
	INNER JOIN public.territoire_ville t on t.id = pp.territory_id
	INNER JOIN public.provinces p on p.id = t.province_id
	group by pp.type
;
-- Quelles sont les capacités de productions des centrales existantes à kongo-central

SELECT ce.id, annee_mise_service, ce.nom, ce.puissance_dispo, ce.nbr_menages_connectes, 
		ce.puissance_installee, p.nom
	FROM public.centrale_electrique ce
	INNER JOIN public.territoire_ville t on t.id = ce.territoire_id
	INNER JOIN public.provinces p on p.id = t.province_id
	WHERE p.id = 2
	;

--- tous les projjet programmés dans le grand kasai

SELECT pp.id, pp."Intitule_projet", pp.puissance, pp.nbr_menages_connectes, pp.type, pp.etat_projet, p.nom as nom_province
	FROM public.projet_programme pp
	INNER JOIN public.territoire_ville t on t.id = pp.territory_id
	INNER JOIN public.provinces p on p.id = t.province_id
	where p.id > 21
;
