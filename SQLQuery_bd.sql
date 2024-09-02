create database Estados 

Create table ciudades(
id int primary key,
nombre varchar(25),
poblacion int,
Fecha_fundacion date,
Historia text)

insert into ciudades (id, nombre, poblacion,fecha_fundacion,historia)
values (1, 'Saltillo', 1234344, '1962-08-01','La ciudad de Saltillo, capital del estado de Coahuila, M�xico, fue fundada en el siglo XVI. Originalmente se llam� "Villa de Santiago del Saltillo" y m�s tarde se uni� con la "Villa de San Esteban de la Nueva Tlaxcala" para formar la ciudad actual. Durante la colonia, Saltillo tuvo un papel importante como centro comercial y religioso.')


insert into ciudades (id, nombre, poblacion,fecha_fundacion,historia)
values (2, 'Torre�n', 1293832, '1876-09-01','La historia de Torre�n se remonta al siglo XIX cuando la regi�n era conocida como �La Laguna�. En 1893, un grupo de visionarios liderados por Francisco Madero adquiri� estas tierras con el objetivo de fundar una ciudad y aprovechar el potencial agr�cola de la zona.')

update ciudades
set nombre= 'Juarez'
where id=1

Create table empresas(
id int,
nombre varchar(25),
id_ciudad int
constraint fk_1 foreign key (id_ciudad) references ciudades(id)

insert into empresas(id, nombre, id_ciudad) values
(26,'polanco',01);

select e.id as empresa, e.nombre as Empresa, c.nombre as Ciudad
from empresas e
inner join ciudades c on e.id_ciudad= c.id;





