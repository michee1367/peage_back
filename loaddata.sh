echo "######################## province beg ##########################"
docker compose exec app flask load-data load-provinces data/new_data/provinces26/Province26.shp
echo "########################## province beg ########################"
echo "######################## territory beg ##########################"
docker compose exec app flask load-data load-territories data/new_data/territories/Territoire.shp
echo "######################## territory end ##########################"

echo "######################## centrale beg ##########################"
docker compose exec app flask load-data load-existing-plant ./data/centrale_existantes_.geojson
echo "######################## centrale end ##########################"

echo "######################## project beg ##########################"
docker compose exec app flask load-data load-project-excel-file data/new_data/projet_planifier.xlsx
docker compose exec app flask load-data load-project-program-excel-file data/new_data/projet_programme.xlsx
echo "######################## project end ##########################"

echo "######################## substation beg ##########################"

docker compose exec app flask load-data load-substation-xlsx  data/noeud.xlsx
docker compose exec app flask load-data load-power-line-xlsx data/ligne_existant.xlsx
docker compose exec app flask load-data load-power-line data/new_data_2/geojsons/lignes_electriques/grid_ht_cc.geojson
docker compose exec app flask load-data load-power-line data/new_data_2/geojsons/lignes_electriques/grid_ht.geojson
docker compose exec app flask load-data load-power-line data/new_data_2/geojsons/lignes_electriques/grid_mt.geojson

echo "######################## substation end ##########################"

echo "######################## demande beg ##########################"
docker compose exec app flask load-data load-demands ./data/Territoires_Villes_Demande_potentielle_Menage_a_electrifier.GEOJSON
echo "######################## demande end ##########################"

echo "######################## health beg ##########################"
docker compose exec app flask load-data load-health-zone data/new_data/zone_sante/OSM_RDC_sante_zones_211212.shp

docker compose exec app flask load-data load-health-instituttion2 data/new_data/structure_sante_2/GRID3_COD_health_facilities_v3_0.shp
docker compose exec app flask load-data load-health-instituttion data/new_data/structure_sante/Structure_sante.shp
echo "######################## health end ##########################"

echo "###################### change coordinates Noeud: Begin ############################"
docker compose exec app flask load-data load-substation-add-coord-xlsx data/postes_coordonnees_decimal.xlsx
echo "###################### change coordinates Noeud: end ############################"


echo "###################### add road : Begin ############################"
docker compose exec app flask load-data load-road data/new_data/route
echo "###################### add road : end ############################"


echo "###################### add education institute  : Begin ############################"
docker compose exec app flask load-data load-eduction flask load-data load-eduction data/new_data/ecole
echo "###################### add education institute : end ############################"

docker compose exec app flask load-data load-cours-eau data/new_data_2/geojsons/cour_eau/
docker compose exec app flask load-data load-localities data/new_data_2/shapefiles/cites/
docker compose exec app flask load-data load-aires-protege data/new_data_2/geojsons/aires_proteges/
docker compose exec app flask load-data load-route data/new_data_2/geojsons/route/

docker compose exec app flask load-data load-mining-zone data/new_data_2/geojsons/mining_site.geojson 
docker compose exec app flask load-data load-eolien-potential-zone data/new_data_2/geojsons/wind.geojson