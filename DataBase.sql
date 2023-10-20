select split_part(noemp,'-',1) as nofinca from cat_empleado;

create database fincaban;
	--SuperUsuario: postgres
	--Contraseña: AH18192001
	--Archivo connectionDB contiene la conexion a la base de datos, se puede cambiar la configuracion

create table finca_install(
	nofinca varchar,
	nombre varchar,
	PRIMARY KEY(nofinca)
);

create table cat_empleado(
	noemp varchar,
	nombre varchar,
	app varchar,
	apm varchar,
	municipio varchar,
	residencia varchar,
	domicilio varchar,
	fecha_nac date,
	correo varchar,
	fecha_registro date,
	area varchar,
	--sexo, edad?
	status varchar(8) CHECK (status IN ('Activo', 'Inactivo', 'No deseado')),
	PRIMARY KEY (noemp)
);

create table document_emp(
	noemp varchar,
	foto_ine bytea,
	foto_comp_dom bytea,
	foto_credencial bytea,
	foto_contrato bytea,
	foto_solicitud bytea,
	PRIMARY KEY(noemp)
);

create table datos_biometricos(
	noemp varchar,
    rostro bytea,
	huella bytea,
	PRIMARY KEY(noemp)
);

create table permisos(
	noemp varchar,
	nopermiso varchar,
	fecha_ini date,
	fecha_fin date,
	observaciones text,
	nofinca varchar,
	PRIMARY KEY(noemp,nopermiso),
	FOREIGN KEY (noemp) REFERENCES cat_empleado(noemp)
);

create table incapacidad(
	noemp varchar,
	noincapacidad varchar,
	fecha_ini date,
	fecha_fin date,
	observaciones text,
	nofinca varchar,
	PRIMARY KEY(noemp,noincapacidad),
	FOREIGN KEY (noemp) REFERENCES cat_empleado(noemp)
);

create table lista_asist(
	noemp varchar,
	fecha date,
	hora_entra time,
	hora_sale time,
	PRIMARY KEY (noemp, fecha),
    FOREIGN KEY (noemp) REFERENCES cat_empleado(noemp)
);